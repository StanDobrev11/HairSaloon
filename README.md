Welcome to HairSaloon WebApp!

1. Purpose and scope:
The main purpose of the website is a booking system with notifications for a Hair Saloon!

The project was developed in order to meet the requirements of SoftUni's Django Advanced course and final project.

It aims to handle bookings by date and time, provide confirmation via email to the client and the hairdresser, and assign to the booking, when created or cancelled.

At the same time, provide an overall view of the available hours to book a service and details of the hairstyles that are available in the saloon.

2. Getting Started:
In order to be able to run the app, please note the requirements.txt file.

3. Usage:
For a regular client, the usage of the app is straightforward -> creating a profile, logging-in, viewing available dates and times, and making or cancel an existing booking;
For a hairdresser, when the profile is created, the admin of the site will provide staff access, and you will be included in the Hairdressers group with certain permissions;
  
4. Features:
The WebApp consists of the following apps:

- accounts -> an extended Django user model using email instead of a username for credentials. When a user is created, a signal is then sent to create OneToOne relation to the Profile object, containing additional profile info.
The app contains various views set to handle user registration, login/logout, password change, and profile edit/delete. The user profile is never deleted from the database, but instead is soft-deleted, triggering the is_active bool to False. When the same user tries to register again with the same email, this will trigger the is_active to True and provide access to the user with the old username. All this is done mainly for training purposes.
The app is tested for custom logic only.

- hairdressers -> the app contains only the model, which is OneToOne related to the user model.
When the user is set to be staff via Admin site, the hairdresser is then created, and the usermodel is associated with it. If a hairdresser is no longer employed in the saloon, i.e. the is_staff is set to False, then hairdresser profile is deleted.

- services -> the idea behind the services app is to contain all the hair styles that can be done by the salon. All the services have a picture of the expected haircut result. The service model has ManyToMany relation to hairdressers since a hairdresser can perform many different hairstyles and a hairstyle can be done by many different hairdressers. The service is added ONLY by the admin of the site after ensuring that a hairdresser can do the haircut. Same goes for the deletion - if a hairdresser, capable of doing certain haircut is fired and there is no one else who can perform that exact haircut, then it should be deleted.
The views are composed in such a way as to ensure proper access. The DeleteServiceView, EditServiceView, and CreateServiceView are accessible only to superusers.
The remaining details and list of service views are available for the general population.

- common -> the common app provides basic views of the index (home page). Without registration, the client is able to access certain features from the home page. The blog page is also accessible. The blog contains all the comments left by registered users. The idea behind a comment is that before becoming visible to the population, the comment is first approved by the administrator. The deletion of the comment can be done either by the client or by the admin. The hairdressers have the option to view the comments.

- api -> this app provides json parsed data to be used for the JS rendered calendar in the bookings section of the webapp. The views, generated the data, are not accessible to unauthorized users.

- bookings -> this is the core of the WebApp, the place where all of the above converge. The created client has access to a calendar view, rendered by JS code with API data. The calendar provides overall information on the available dates/times to make a booking. The form for creating a booking is not generated on a separate view but is generated on the same template.
The procedure for making a booking is simple. When a stylist is selected, the calendar will display their occupied hours and prevent overlapping.
The free cells are available for booking. The date/time are auto-filled on the form, and when the desired service is selected, the duration will be calculated as the expected end time.
The option for canceling bookings lies in the hands of the client and the hairdresser. The cancellation of a booking is actually done by altering the bool field cancelled to True. This will ensure that the hairdresser will be able to view all cancellations beforehand on their calendar.
When a booking is first created or cancelled, a notification email is sent to the client and to the hairdresser booked for the service. The email service is async-coded using Celery, Redis and MailHog to simulate SMTP server. All three apps are then run in a Docker container. The same email service can be extended to cover the creation of the client profile as a welcome message and for the rest of the apps. The The sending of an email is triggered after saving a booking.
The hairdresser has a view of their respective bookings only without any concern about the workflow of their coworkers. The admin has a complete view of all bookings currently made, excluding cancelled bookings.

5. Deployment
Not yet developed the deployment of the project.
