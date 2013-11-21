create table hop (
	id integer primary key autoincrement,
	name string not null unique,
    websafe_name not null unique,
	alpha_acid string not null,
	description text
);

create table beer_style (
	id integer primary key autoincrement,
	name string not null unique,
	description text
);

create table hop_style_map (
	hop_id integer references hop(id),
	style_id integer references beer_style(id),
	primary key (hop_id, style_id)
);

create table hop_combination (
	hop_one_id integer references hop(id),
	hop_two_id integer references hop(id),
	primary key (hop_one_id, hop_two_id)
);

create table hop_alternative (
	hop_id integer references hop(id),
	alternative_id integer references hop(id),
	primary key (hop_id)
);

