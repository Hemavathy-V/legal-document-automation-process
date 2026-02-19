"""
Template Parser Module
Extracts placeholders from DOCX contract templates and collects user inputs
Supports both simple placeholders and Handlebars/Mustache-style loops
"""

import re
import json
from datetime import datetime
from pathlib import Path
from docx import Document
from typing import Dict, List, Any, Tuple


class TemplateParser:
    """Parse DOCX templates and extract placeholders with proper handling of loops"""
    
    def __init__(self, template_path: Path):
        """
        Initialize parser with a template file
        
        Args:
            template_path: Path to the DOCX template file
        """
        self.template_path = Path(template_path)
        self.template_text = self._load_template()
        self.simple_placeholders = []
        self.loop_placeholders = {}
        self._extract_all_placeholders()
    
    def _load_template(self) -> str:
        """Load and extract text from DOCX template"""
        doc = Document(self.template_path)
        # Extract text from all paragraphs
        full_text = "\n".join([para.text for para in doc.paragraphs])
        return full_text
    
    def _extract_all_placeholders(self) -> None:
        """Extract both simple and loop placeholders from template"""
        # Extract loop placeholders: {{#fieldName}}...{{/fieldName}}
        loop_pattern = r"\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}"
        loop_matches = re.findall(loop_pattern, self.template_text, re.DOTALL)
        
        for loop_field, loop_content in loop_matches:
            # Extract nested fields within the loop
            nested_pattern = r"\{\{(\w+)\}\}"
            nested_fields = re.findall(nested_pattern, loop_content)
            self.loop_placeholders[loop_field] = nested_fields
        
        # Extract simple placeholders: {{fieldName}}
        # But exclude those already in loops
        simple_pattern = r"\{\{([\w.]+)\}\}"
        simple_matches = re.findall(simple_pattern, self.template_text)
        
        # Filter out loop declarations
        for match in simple_matches:
            if match not in self.loop_placeholders:
                if match not in self.simple_placeholders:
                    self.simple_placeholders.append(match)
    
    def get_simple_placeholders(self) -> List[str]:
        """Get list of simple placeholders"""
        return self.simple_placeholders
    
    def get_loop_placeholders(self) -> Dict[str, List[str]]:
        """Get dictionary of loop placeholders with their nested fields"""
        return self.loop_placeholders
    
    def get_all_placeholders(self) -> Tuple[List[str], Dict[str, List[str]]]:
        """Get both simple and loop placeholders"""
        return self.simple_placeholders, self.loop_placeholders
    
    def get_template_filename(self) -> str:
        """Get template filename without extension"""
        return self.template_path.stem.replace("-Template", "").replace("-", "")


class InputCollector:
    """Collect user inputs for contract placeholders"""
    
    def __init__(self, simple_placeholders: List[str], loop_placeholders: Dict[str, List[str]]):
        """
        Initialize input collector
        
        Args:
            simple_placeholders: List of simple placeholder fields
            loop_placeholders: Dictionary of loop fields with nested fields
        """
        self.simple_placeholders = simple_placeholders
        self.loop_placeholders = loop_placeholders
        self.user_data = {}
    
    def _format_field_name(self, field: str) -> str:
        """
        Convert field names to readable questions
        E.g., 'effectiveDate' -> 'Effective Date'
        """
        # Handle dot notation (e.g., 'deliverable.name' -> 'deliverable name')
        field = field.replace("_", " ").replace(".", " ")
        
        # Add space before capital letters (camelCase)
        field = re.sub(r'([a-z])([A-Z])', r'\1 \2', field)
        
        return field.strip()
    
    def collect_simple_inputs(self) -> Dict[str, str]:
        """Collect inputs for simple placeholders"""
        print("\n" + "="*70)
        print("COLLECTING CONTRACT INFORMATION")
        print("="*70 + "\n")
        
        for placeholder in self.simple_placeholders:
            field_name = self._format_field_name(placeholder)
            prompt = f"{field_name}: "
            
            while True:
                user_input = input(prompt).strip()
                if user_input:
                    self.user_data[placeholder] = user_input
                    break
                else:
                    print("This field cannot be empty. Please enter a value.")
        
        return self.user_data
    
    def collect_loop_inputs(self) -> Dict[str, List[Dict[str, str]]]:
        """Collect inputs for loop-based sections"""
        loop_data = {}
        
        for loop_name, nested_fields in self.loop_placeholders.items():
            print(f"\n{'-'*70}")
            print(f"Section: {self._format_field_name(loop_name)}")
            print(f"{'-'*70}")
            
            items = []
            count = 1
            
            while True:
                print(f"\nEntry {count}:")
                item_data = {}
                
                for field in nested_fields:
                    field_name = self._format_field_name(field)
                    prompt = f"  {field_name}: "
                    
                    user_input = input(prompt).strip()
                    if user_input:
                        item_data[field] = user_input
                
                if item_data:
                    items.append(item_data)
                
                # Ask if user wants to add another entry
                add_more = input("\nAdd another entry? (y/n): ").strip().lower()
                if add_more != 'y':
                    break
                
                count += 1
            
            if items:
                loop_data[loop_name] = items
        
        return loop_data
    
    def get_all_inputs(self) -> Dict[str, Any]:
        """Collect all inputs (simple + loops) and return combined dictionary"""
        # Collect simple placeholders
        self.collect_simple_inputs()
        
        # Collect loop-based inputs
        if self.loop_placeholders:
            loop_data = self.collect_loop_inputs()
            self.user_data.update(loop_data)
        
        return self.user_data


class ContractProcessor:
    """Main processor for contract template selection and JSON generation"""
    
    def __init__(self, templates_dir: Path, output_dir: Path):
        """
        Initialize processor
        
        Args:
            templates_dir: Directory containing DOCX templates
            output_dir: Directory for saving JSON outputs
        """
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def list_available_templates(self) -> List[Path]:
        """List all available DOCX templates"""
        templates = list(self.templates_dir.glob("*.docx"))
        return sorted(templates)
    
    def select_template(self) -> Path:
        """
        Display templates and let user select one
        
        Returns:
            Path to selected template
        """
        templates = self.list_available_templates()
        
        if not templates:
            print("No templates found in the templates directory!")
            return None
        
        print("\n" + "="*70)
        print("AVAILABLE CONTRACT TEMPLATES")
        print("="*70 + "\n")
        
        for idx, template in enumerate(templates, 1):
            template_name = template.stem.replace("-Template", "").replace("-", " ")
            print(f"  {idx}. {template_name}")
        
        while True:
            try:
                choice = input(f"\nSelect template (1-{len(templates)}): ").strip()
                choice_idx = int(choice) - 1
                
                if 0 <= choice_idx < len(templates):
                    return templates[choice_idx]
                else:
                    print(f"Please enter a number between 1 and {len(templates)}")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def process_contract(self) -> bool:
        """
        Main workflow: select template, extract placeholders, collect inputs, save JSON
        
        Returns:
            True if successful, False otherwise
        """
        # Step 1: Select template
        template_path = self.select_template()
        if not template_path:
            return False
        
        print(f"\nSelected: {template_path.stem}")
        
        # Step 2: Parse template
        try:
            parser = TemplateParser(template_path)
            simple_placeholders, loop_placeholders = parser.get_all_placeholders()
            template_name = parser.get_template_filename()
            
            print(f"Found {len(simple_placeholders)} simple fields")
            if loop_placeholders:
                print(f"Found {len(loop_placeholders)} repeating sections")
        except Exception as e:
            print(f"Error parsing template: {e}")
            return False
        
        # Step 3: Collect inputs
        try:
            collector = InputCollector(simple_placeholders, loop_placeholders)
            user_data = collector.get_all_inputs()
        except KeyboardInterrupt:
            print("\n\nProcess cancelled by user.")
            return False
        except Exception as e:
            print(f"Error collecting inputs: {e}")
            return False
        
        # Step 4: Save to JSON
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{template_name}_{timestamp}.json"
            filepath = self.output_dir / filename
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=4, ensure_ascii=False)
            
            print("\n" + "="*70)
            print("SUCCESS!")
            print("="*70)
            print(f"\nContract data saved to:")
            print(f"   {filepath}")
            print(f"\nTotal fields collected: {self._count_fields(user_data)}")
            print("="*70 + "\n")
            return True
        
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    @staticmethod
    def _count_fields(data: Dict) -> int:
        """Count total number of fields in collected data"""
        count = 0
        for value in data.values():
            if isinstance(value, list):
                count += sum(len(item) if isinstance(item, dict) else 1 for item in value)
            else:
                count += 1
        return count


def main():
    """Main entry point"""
    # Setup paths
    current_dir = Path(__file__).parent
    templates_dir = current_dir.parent.parent.parent / "sample_templates"
    output_dir = current_dir.parent.parent / "output"
    
    # Process contract
    processor = ContractProcessor(templates_dir, output_dir)
    processor.process_contract()


if __name__ == "__main__":
    main()
