-- B-Bot Supabase Database Setup Script
-- Run this in your Supabase project's SQL Editor

-- Enable UUID extension for generating unique IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create save_states table
CREATE TABLE IF NOT EXISTS save_states (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    grid_json JSONB NOT NULL,
    wood_count INTEGER DEFAULT 0,
    stone_count INTEGER DEFAULT 0,
    population_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_save_states_user_id ON save_states(user_id);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE save_states ENABLE ROW LEVEL SECURITY;

-- RLS Policies for users table
-- Allow anyone to insert new users (for registration)
CREATE POLICY "Allow public registration" ON users
    FOR INSERT
    TO anon
    WITH CHECK (true);

-- Allow authenticated users to read their own user data
CREATE POLICY "Users can read own data" ON users
    FOR SELECT
    TO authenticated
    USING (auth.uid()::text = id::text);

-- RLS Policies for save_states table
-- Allow authenticated users to insert their own save states
CREATE POLICY "Users can insert own save states" ON save_states
    FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid()::text = user_id::text);

-- Allow authenticated users to read their own save states
CREATE POLICY "Users can read own save states" ON save_states
    FOR SELECT
    TO authenticated
    USING (auth.uid()::text = user_id::text);

-- Allow authenticated users to update their own save states
CREATE POLICY "Users can update own save states" ON save_states
    FOR UPDATE
    TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

-- Allow authenticated users to delete their own save states
CREATE POLICY "Users can delete own save states" ON save_states
    FOR DELETE
    TO authenticated
    USING (auth.uid()::text = user_id::text);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update updated_at on save_states
CREATE TRIGGER update_save_states_updated_at
    BEFORE UPDATE ON save_states
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON TABLE users TO anon, authenticated;
GRANT ALL ON TABLE save_states TO authenticated;
