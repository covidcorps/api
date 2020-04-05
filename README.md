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

battles: Locations where the help is needed
GET         /battles/
POST        /battles/
PATCH       /battles/:id
GET         /battles/:id

deployments: Requests for help from specific battles. Always associated with a specific site.
GET         /battles/:id/deployments
GET         /battles/:site_id/deployments/:dep_id
POST        /battles/:id/deployments/
PATCH       /battles/:site_id/deployments/:dep_id
DELETE      /battles/:site_id/deployments/:dep_id
GET         /battles/:site_id/deployments/:dep_id/assignments

assignments: A link between a corpsmember and a specific deployment. Allows corpsmembers to accept/reject assignments
GET         /corpsmembers/:id/assignments
POST        /corpsmembers/:id/assignments
GET         /corpsmembers/:member_id/assignments/:assignment_id
PUT         /corpsmembers/:member_id/assignments/:assignment_id
PATCH       /corpsmembers/:member_id/assignments/:assignment_id
DELETE      /corpsmembers/:member_id/assignments/:assignment_id


```