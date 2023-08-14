drop table if exists users;
create table users (
    id uuid primary key default gen_random_uuid(),
    name text,
    real_name text,
    google_email text,
    google_request_id text,
    next_action json
);

drop table if exists user_results;
create table user_results (
    user_id uuid not null,
    puzzle_id text not null default 'test',
    duration_secs int4,
    foreign key(user_id) references users(id),
    unique (user_id, puzzle_id)
);
