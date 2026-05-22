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
    metal_count INTEGER DEFAULT 0,
    energy_count INTEGER DEFAULT 0,
    population_count INTEGER DEFAULT 0,
    bot_x INTEGER DEFAULT 0,
    bot_y INTEGER DEFAULT 0,
    bot_direction TEXT DEFAULT 'RIGHT',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_save_states_user_id ON save_states(user_id);

-- Row Level Security
-- Note: RLS is disabled for both tables since we use custom JWT authentication
-- Security is handled by our backend authentication system
-- Supabase RLS is designed for Supabase Auth, not custom JWT

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
