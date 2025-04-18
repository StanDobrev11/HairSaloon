## Welcome to HairSaloon WebApp!

### Purpose and Scope: 
The main purpose of the website is to serve as a booking system with notifications for a Hair Saloon. The project was developed to meet the requirements of SoftUni's Django Advanced course and final project.

It aims to handle bookings by date and time, provide confirmation via email to the client and the hairdresser, and assign bookings when created or canceled.

At the same time, it provides an overall view of the available hours to book a service and details of the hairstyles that are available in the salon.

### Getting Started: 
To run the app, please note the requirements.txt file.

### Usage: 
For a regular client, the usage of the app is straightforward: creating a profile, logging in, viewing available dates and times, and making or canceling an existing booking. For a hairdresser, once the profile is created, the site admin will provide staff access, and the hairdresser will be included in the Hairdressers group with certain permissions.

### Features: 
The WebApp consists of the following apps:

- **accounts**: This app features an extended Django user model using email instead of a username for credentials. When a user is created, a signal is sent to create a OneToOne relation to the Profile object, which contains additional profile info. The app has various views to handle user registration, login/logout, password change, and profile edit/delete. The user profile is never deleted from the database; instead, it is soft-deleted by setting the is_active boolean to False. If the same user tries to register again with the same email, this will set is_active to True and provide access to the user with the old username. All this is done mainly for training purposes. The app is tested for custom logic only.

- **hairdressers**: This app contains only the model, which is OneToOne related to the user model. When the user is set to be staff via the Admin site, the hairdresser is then created, and the user model is associated with it. If a hairdresser is no longer employed in the salon (i.e., the is_staff is set to False), then the hairdresser profile is deleted.

- **services**: The services app contains all the hairstyles that can be done by the salon. All services have a picture of the expected haircut result. The service model has a ManyToMany relation to hairdressers since a hairdresser can perform many different hairstyles, and a hairstyle can be done by many different hairdressers. The service is added ONLY by the admin of the site after ensuring that a hairdresser can perform the haircut. The same applies to deletion; if a hairdresser capable of doing a certain haircut is fired and there is no one else who can perform that haircut, it should be deleted. The views are composed to ensure proper access. The DeleteServiceView, EditServiceView, and CreateServiceView are accessible only to superusers. The remaining details and list of service views are available for the general population.

- **common**: The common app provides basic views of the index (home page). Without registration, the client can access certain features from the home page. The blog page is also accessible. The blog contains all the comments left by registered users. Comments must be approved by the administrator before becoming visible to the public. Deletion of the comment can be done either by the client or by the admin. Hairdressers have the option to view the comments.

- **api**: This app provides JSON-parsed data to be used for the JS-rendered calendar in the bookings section of the web app. The views generating the data are not accessible to unauthorized users.

- **bookings**: This is the core of the WebApp, where all of the above converge. The created client has access to a calendar view, rendered by JS code with API data. The calendar provides overall information on the available dates and times to make a booking. The form for creating a booking is not generated on a separate view but rather on the same template. The booking procedure is simple: when a stylist is selected, the calendar will display their occupied hours and prevent overlapping. The free slots are available for booking. The date/time are auto-filled on the form, and when the desired service is selected, the expected end time is calculated based on the duration. The option for canceling bookings lies with both the client and the hairdresser. The cancellation of a booking is done by altering the boolean field "cancelled" to True. This ensures that the hairdresser can view all cancellations beforehand on their calendar. When a booking is created or canceled, a notification email is sent to both the client and the hairdresser booked for the service. The email service is async-coded using Celery, Redis, and MailHog to simulate an SMTP server. All three apps run in a Docker container. The same email service can be extended to cover the creation of the client profile as a welcome message and for the rest of the apps. The sending of an email is triggered after saving a booking. The hairdresser has a view of their respective bookings only, without concern for the workflow of their coworkers. The admin has a complete view of all currently made bookings, excluding canceled bookings.

### Deployment: 
The project has been deployed at the following address: https://hairsalon.cloudmachine.uk/. 

The app is hosted on a virtual machine on my private server and deployed using Docker

Once a booking has been created or deleted, an email is sent to the user as notification. In order to test the service, make sure you register with a valid email address.
