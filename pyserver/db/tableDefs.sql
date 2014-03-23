
create table `CriminalLocation` ( 
    `id` integer not null primary key auto_increment, 
    `PostedTime` TIMESTAMP NOT NULL, 
    `lat` float null, 
    `lng` float null, 
    `route` varchar(128),
    `sublocality` varchar(128),
    `city` varchar(128), 
    `country` varchar(128)
);

create table `VictimLocation` ( 
    `id` integer not null primary key auto_increment, 
    `PostedTime` TIMESTAMP NOT NULL, 
    `lat` float null, 
    `lng` float null, 
    `route` varchar(128),
    `sublocality` varchar(128),
    `city` varchar(128), 
    `country` varchar(128)
);
