update pg_database
set encoding = pg_char_to_encoding('UTF8')
where datname = 'puzzles_db';

show server_encoding;
show client_encoding;

drop table if exists users;
create table users (
    id uuid primary key default gen_random_uuid(),
    name text,
    real_name text,
    google_email text,
    google_request_id text,
    next_action json
);

drop table if exists puzzles;
create table puzzles (
    id text primary key,
    preview text,
    metadata text,
    name text,
    duration_ms int4
);

insert into puzzles (id, preview, metadata, name, duration_ms)
values
    ('test', '/data/preview/test.gif', '/data/2/puzzle-metadata.json', 'Big Buck Bunny', 5000),
    ('nu_pogody', '/data/preview/nu_pogody.gif', '/data/4/puzzle-metadata.json', 'Ну, погоди!', 26820);

drop table if exists user_results;
create table user_results (
    user_id uuid not null,
    puzzle_id text not null default 'test',
    duration_secs int4,
    foreign key(user_id) references users(id),
    foreign key(puzzle_id) references puzzles(id),
    unique (user_id, puzzle_id)
);
