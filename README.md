Welcome to HairSaloon WebApp!

1. Purpose and scope:
The main purpose of the website is a booking system with notifications for a Hair Saloon!

The project is developed in order to meet the requirements of the SoftUni's Django Advanced course and final project.
It aims to handle bookings by date and time, provide confirmation via email to the client and the hairdresser, assigned
to the booking, when created or cancelled.

At the same time provide overall view of the available hours to book a service and details of the hairstyles, 
that are available in the saloon.

2. Getting Started:
In order to be able to run the app, please note the requirements.txt file.

3. Usage:
For a regular client, the usage of the app is straightforward -> creating a profile, logging-in, view available date/times and make or
cancel existing booking;
For a hairdresser, when the profile is created, the admin of the site will provide staff access and you will be included in the Hairdressers
group with certain permissions;
  
4. Features:
The WebApp consist of following apps:

- accounts -> an extended Django usermodel, using email instead of username for credentials. When user is created, a signal is then send to
create OneToOne relation to Profile object, containing additional profile info.
The app contains various views set to handle user registration, login/logout, password change and profile edit/delete. The user profile is never
deleted from the database, but instead is soft-deleted, triggering the is_active bool to False.
When the same user tries to register again with the same email, this will trigger the is_active to True and provide access to the user with
the old username.
All this is done mainly for training purpose.
The app is tested for custom logic only.

- hairdressers -> the app contains only the model which is OneToOne related to the usermodel.
When the user is set to be staff via Admin site, the hairdresser is then created and the usermodel assocciated with it. If a hairdresser is
no longer employed in the saloon, i.e. the is_staff is set to False, then hairdresser profile is deleted.

- services -> the idea behind the services app is containing all hair styles that can be done by the saloon. All the services have a picture of
the expected haircut result. The service model has ManyToMany relation to hairdressers since a hairdresser can perform many different
hairstyles and a hairstyle can be done by many different hairdressers. The service is added ONLY by the admin of the site after ensuring that
a hairdresser can do the haircut. Same goes for the deletion - if hairdresser, capable of doing certain haircut is fired and there is no one
else who can perform that exact haircut, then it should be deleted.
The views are composed in such a way to ensure proper access. The DeleteServiceView, EditServiceView and CreateServiceView are accessible only to superusers.
The remaining details and list service views are available for general population.

- common -> the common app provides basic views of the index (home page). Wthout registration, the client is able to access certain features from
the home page. The blog page is also accessible. The blog contains all the comments left by registered users. The idea behind a comment is that
before becoming visible to the population, the comment is first approved by admin. The deletion of the comment can be done either by the client or
by the admin. The hairdressers have the option to view the comments.

- api -> this app provides json parsed data to be used for the JS rendered calendar on the bookings section of the webapp. The views, generating
the data, are not accessible to unauthorised users.

- bookings -> this is the core of the WebApp, the place where all of above converge. The created clien has access to calendar view, rendered by JS
code with API data. The calendar provides overall information of the available dates/times to make a booking. The form for creating booking is
not generated on separate view but is generated on the same template using JS. When a date/time cell is selected, the start time is set in the form,
when a service is selected, the end time is autocompleted using JS. When the form is saved, attempt is made to filter
Examples: Code snippets or links to examples demonstrating how to use the project or its key features.
6. Contribution Guidelines
How to Contribute: Instructions for potential contributors on how to suggest improvements, submit pull requests, or report bugs.
Code of Conduct: A link to the project's code of conduct.
Community and Communication: Information on how to get in touch, such as links to community forums, project mailing lists, or chat rooms.
7. Documentation
API Documentation: If applicable, links to API documentation or how to generate it.
Architectural Overview: An optional high-level overview of the architecture, for more complex projects.
Further Reading: Links to any further documentation or tutorials.
8. Testing
Running Tests: Instructions on how to run the project's test suite.
Writing Tests: Guidelines for writing tests for the project.
9. Deployment
Deployment Methods: Instructions on how to deploy the project in a production environment.
Environment Variables: A list of environment variables that need to be set for deployment.
10. Credits and Acknowledgments
Authors and Contributors: Information about the project's authors and contributors.
Acknowledgments: Credits to any third-party services, libraries, or code used in the project.
Licensing: The project's license, often with a link to the full text.
11. Additional Sections
Screenshots/Demos: Links to screenshots or demos of your project in action.
FAQs: Answers to frequently asked questions.
Known Issues: Any known issues or limitations of the project.
Collecting the Information
Before writing the README, ensure you have all the necessary information. This might involve:

Reviewing your project documentation.
Discussing with team members or contributors to capture all features and instructions.
Testing the installation and usage instructions in a clean environment to ensure they work as described.
Having gathered all this information, you’re well-equipped to write a README that effectively communicates your project’s value and how to engage with it. Remember, a good README is often a collaborative effort that evolves along with your project.
