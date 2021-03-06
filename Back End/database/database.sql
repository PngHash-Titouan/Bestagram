DROP DATABASE Bestagram;
CREATE DATABASE Bestagram;
USE Bestagram;

CREATE TABLE UserTable(
    id BIGINT NOT NULL AUTO_INCREMENT,
    username VARCHAR(30) NOT NULL,
    name VARCHAR(50) NOT NULL,
    hash VARCHAR(64) NOT NULL,
    email VARCHAR(150) NOT NULL,
    public_profile BOOLEAN DEFAULT TRUE,
    token VARCHAR(200),
    refresh_token VARCHAR(200) NOT NULL,
    token_registration_date DATETIME,
    caption VARCHAR(1000),
    use_default_picture BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id)
)
ENGINE=INNODB;

CREATE TABLE LikeTable(
    user_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL
)
ENGINE=INNODB;

CREATE TABLE Post(
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    post_time DATETIME NOT NULL,
    caption VARCHAR(2200),
    PRIMARY KEY(id)
)
ENGINE=INNODB;

CREATE TABLE Follow(
    user_id BIGINT NOT NULL,
    user_id_followed BIGINT NOT NULL
)
ENGINE=INNODB;

CREATE TABLE Tag(
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    x_pos FLOAT NOT NULL,
    y_pos FLOAT NOT NULL
)
ENGINE=INNODB;

-- Indexes
ALTER TABLE UserTable
ADD UNIQUE ind_username (username);

ALTER TABLE UserTable
ADD UNIQUE ind_email (email);

ALTER TABLE UserTable
ADD INDEX ind_name (name);

ALTER TABLE UserTable
ADD UNIQUE ind_token (token);

ALTER TABLE UserTable
ADD UNIQUE ind_refresh_token (refresh_token);

ALTER TABLE LikeTable
ADD UNIQUE ind_user_id_post_id (user_id, post_id);

ALTER TABLE LikeTable
ADD INDEX ind_user_id (user_id);

ALTER TABLE LikeTable
ADD INDEX ind_post_id (post_id);

ALTER TABLE Follow
ADD UNIQUE ind_user_id_user_id_followed (user_id, user_id_followed);

ALTER TABLE Follow
ADD INDEX ind_user_id (user_id);

ALTER TABLE Follow
ADD INDEX ind_user_id_followed (user_id_followed);

ALTER TABLE Post
ADD INDEX ind_user_id (user_id);

ALTER TABLE Tag
ADD INDEX ind_user_id (user_id);

ALTER TABLE Tag
ADD INDEX ind_post_id (post_id);

-- Foreign Keys

ALTER TABLE LikeTable
ADD CONSTRAINT fk_LikeTable_user_id_id FOREIGN KEY (user_id) REFERENCES UserTable(id);

ALTER TABLE LikeTable
ADD CONSTRAINT fk_LikeTable_post_id_id FOREIGN KEY (post_id) REFERENCES Post(id);

ALTER TABLE Follow
ADD CONSTRAINT fk_Follow_user_id_id FOREIGN KEY (user_id) REFERENCES UserTable(id);

ALTER TABLE Follow
ADD CONSTRAINT fk_Follow_user_id_followed_id FOREIGN KEY (user_id_followed) REFERENCES UserTable(id);

ALTER TABLE Post
ADD CONSTRAINT fk_Post_user_id_id FOREIGN KEY (user_id) REFERENCES UserTable(id);

ALTER TABLE Tag
ADD CONSTRAINT fk_Tag_user_id_id FOREIGN KEY (user_id) REFERENCES UserTable(id);

ALTER TABLE Tag
ADD CONSTRAINT fk_Tag_post_id_id FOREIGN KEY (post_id) REFERENCES Post(id);
