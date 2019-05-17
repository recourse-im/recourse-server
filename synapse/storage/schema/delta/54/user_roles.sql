-- The roles users have in groups
CREATE TABLE user_roles (
    user_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    role_id TEXT NOT NULL,
    profile TEXT NOT NULL,
    is_public BOOLEAN NOT NULL,  -- whether the role should be show to everyone
    UNIQUE (user_id, role_id)
);
