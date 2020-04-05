# CovidCorps Web Service

> © 2020 Brett Arkin and GigaBryte LLC - All Rights Reserved

## API

The CovidCorps service provides a ReSTful API

```
corpsmembers: Doctors, nurses, and other volunteers who have signed up
GET         /corpsmembers/
POST        /corpsmembers/
GET         /corpsmembers/:id
PUT         /corpsmembers/:id
PATCH       /corpsmembers/:id
DELETE      /corpsmembers/:id

locations: Locations where the help is needed
GET         /locations/
POST        /locations/
PATCH       /locations/:id
GET         /locations/:id

deployments: Requests for help from specific locations. Always associated with a specific site.
GET         /locations/:id/deployments
GET         /locations/:loc_id/deployments/:dep_id
POST        /locations/:id/deployments/
PATCH       /locations/:loc_id/deployments/:dep_id
DELETE      /locations/:loc_id/deployments/:dep_id
GET         /locations/:loc_id/deployments/:dep_id/assignments

assignments: A link between a corpsmember and a specific deployment. Allows corpsmembers to accept/reject assignments
GET         /corpsmembers/:id/assignments
POST        /corpsmembers/:id/assignments
GET         /corpsmembers/:member_id/assignments/:assignment_id
PUT         /corpsmembers/:member_id/assignments/:assignment_id
PATCH       /corpsmembers/:member_id/assignments/:assignment_id
DELETE      /corpsmembers/:member_id/assignments/:assignment_id


```


## Database

The CovidCorps web service uses Google Cloud Spanner as it's primary relational database for the storage of corpsmember and battle information.

```

Table: accounts
Secure auth info for corpsmembers and locations
id                  INT PK
email               VARCHAR
password            VARCHAR         -- Secured by hash
created_ts          TIMESTAMP
last_ts             TIMESTAMP

--------------------------------------

Table: corpsmembers
Members of the CovidCorps. Doctors, nurses and others.
id                  INT PK
account_id          INT FK
prefix              VARCHAR
firstname           VARCHAR
middlename          VARCHAR
lastname            VARCHAR
address1            VARCHAR
address2            VARCHAR
city                VARCHAR
state               ENUM
zipcode             VARCHAR(5)
suffix              VARCHAR
status              ENUM(active, inactive, deceased)
joined_ts           TIMESTAMP
last_ts             TIMESTAMP

--------------------------------------

Table: corpsmembers_contact_options
Contact info for corpsmembers
id                  INT PK
corpsmember_id      INT FK
type                ENUM(phone, email)
value               VARCHAR
primary             BOOL
created_ts          TIMESTAMP
last_ts             TIMESTAMP

--------------------------------------

Table: locations
The locations that are requesting assistance
id                  INT PK
account_id          INT FK
name                VARCHAR
address1            VARCHAR
address2            VARCHAR
city                VARCHAR
state               ENUM
zipcode             VARCHAR(5)
lat                 double
lng                 double
created_ts          TIMESTAMP
last_ts             TIMESTAMP

--------------------------------------

Table: deployments
Requests for help from locations
id                      INT PK
location_id             INT FK
reason                  TEXT
num_corpsmembers        INT
created_ts              TIMESTAMP
last_ts                 TIMESTAMP

--------------------------------------

Table: corpsmembers_deployments
Associative table. Connects corps members with deployments and indicates whether they have accepted the assignment
corpsmember_id          INT FK
deployment_id           INT FK
status                  ENUM(pending, accepted, enroute, onsite, complete)
last_ts                 TIMESTAMP
```



> Note: Need an alternative persistence solution for tracking account login attempts and successes for security.