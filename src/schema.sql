-- Table: schools
CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL,
    acronym VARCHAR(10)
);

-- Table: links
CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    link VARCHAR(120) UNIQUE NOT NULL
);

-- Table: locations
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country VARCHAR(120) DEFAULT 'North Cyprus',
    city VARCHAR(120),
    area VARCHAR(120)
);

-- Table: usergrouping
CREATE TABLE IF NOT EXISTS usergrouping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_max_count INTEGER,
    group_count_status INTEGER,
    link_id INTEGER REFERENCES links(id)
);

-- Table: users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(120) UNIQUE NOT NULL,
    fname VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    username VARCHAR(120) NOT NULL,
    profile_description VARCHAR(1024),
    gender VARCHAR(10) CHECK (gender IN ('male', 'female')) NOT NULL,
    profile_photo VARCHAR(2048),
    uni_major VARCHAR(1024),
    year_of_school VARCHAR(1) CHECK (year_of_school IN ('0', '1', '2'))  DEFAULT '0',
    user_type VARCHAR(20) CHECK (user_type IN ('ordinary_user', 'admin'))  DEFAULT 'ordinary_user',
    password_hash VARCHAR(512),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_validated BOOLEAN DEFAULT 0,
    num_posts INTEGER DEFAULT 0,
    school INTEGER REFERENCES schools(id),
    user_group INTEGER REFERENCES usergrouping(id)
);

-- Table: posts
CREATE TABLE IF NOT EXISTS  posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    room_count VARCHAR(120),
    monthly_rent INTEGER,
    currency VARCHAR(30),
    non_advance_monthly_rent INTEGER DEFAULT 0,
    move_in_rent INTEGER DEFAULT 0,
    from_owner BOOLEAN DEFAULT 0,
    bills_included_on_rent BOOLEAN DEFAULT 0,
    deposit_factor INTEGER DEFAULT 1,
    commission_factor INTEGER DEFAULT 1,
    payment_interval INTEGER,
    post_type VARCHAR(30) CHECK (post_type IN ('need_roommate', 'need_room_and_roommate')) NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    user_id INTEGER REFERENCES users(id),
    ad_link VARCHAR(120),
    city VARCHAR(1024),
    village VARCHAR(1024)
    --- location_id INTEGER REFERENCES locations(id),
    --- location_string VARCHAR(1024)
);

-- Table: messages
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message VARCHAR(1024),
    sender_id INTEGER REFERENCES users(id),
    recepient_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: email_validation
CREATE TABLE IF NOT EXISTS email_validation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(1024),
    expiry_date TIMESTAMP
);

-- Create indexes
CREATE INDEX  IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX  IF NOT EXISTS idx_users_fname ON users(fname);
CREATE INDEX  IF NOT EXISTS idx_users_school ON users(school);
CREATE INDEX  IF NOT EXISTS idx_users_group ON users("group");
CREATE INDEX  IF NOT EXISTS idx_posts_user_id ON posts(user_id);
CREATE INDEX  IF NOT EXISTS idx_posts_city ON posts(city);
CREATE INDEX  IF NOT EXISTS idx_posts_village ON posts(village);
CREATE INDEX  IF NOT EXISTS idx_posts_ad_link ON posts(ad_link);
CREATE INDEX  IF NOT EXISTS idx_posts_is_active ON posts(is_active);
CREATE INDEX  IF NOT EXISTS idx_posts_post_type ON posts(post_type);
CREATE INDEX  IF NOT EXISTS idx_posts_created_at ON posts(created_at);
CREATE INDEX  IF NOT EXISTS idx_messages_sender_id ON messages(sender_id);
CREATE INDEX  IF NOT EXISTS idx_messages_recepient_id ON messages(recepient_id);
CREATE INDEX  IF NOT EXISTS idx_messages_created_at ON messages(created_at);
