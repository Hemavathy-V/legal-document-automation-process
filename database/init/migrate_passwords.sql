-- Migration: widen password column and re-hash all plain-text seed passwords
-- Run this ONLY on an existing database that was set up before password hashing was introduced.
-- Safe to run multiple times (ALTER COLUMN is idempotent for widening).
--
-- Plaintext password being replaced: Password1
-- Bcrypt hash (cost 12) for Password1:
--   $2b$12$w/ReoleEVuYj0dU4JKmQ6OVGuqWR8ITSW0FGOdaiZiZ0zh9TXdSAC

USE contract_management1;

-- Step 1: widen the password column to hold bcrypt hashes (60 chars; 255 for future-proofing)
ALTER TABLE users MODIFY COLUMN password VARCHAR(255) NULL;

-- Step 2: replace plain-text 'Password1' with its bcrypt hash for all seed users
UPDATE users
SET password = '$2b$12$w/ReoleEVuYj0dU4JKmQ6OVGuqWR8ITSW0FGOdaiZiZ0zh9TXdSAC'
WHERE password = 'Password1';
