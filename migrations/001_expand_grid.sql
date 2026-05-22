-- Migration script to expand grid from 10x10 to 20x20 and add new resource fields
-- Run this in your Supabase project's SQL Editor to migrate existing databases

-- Add new resource columns to save_states table
ALTER TABLE save_states 
ADD COLUMN IF NOT EXISTS metal_count INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS energy_count INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS bot_x INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS bot_y INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS bot_direction TEXT DEFAULT 'RIGHT';

-- Note: Existing grid_json data will remain as-is. When users load their old saves,
-- the frontend will need to handle 10x10 grids gracefully or reset to the new 20x20 format.
-- The application logic will handle the transition automatically.
