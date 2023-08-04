# Requirements

## Functional Requirements

---

The functional requirements section outlines all of the essential requirements for the Clean Energy PA Application. They are the core requirements that will drive the development of the application.

### 1.1.1 User Registration

- 1.1.1.1. The system shall allow the user to create an account.
- 1.1.1.2. The system registration shall collect the user’s name.
- 1.1.1.3. The system registration shall collect the user’s email address.
- 1.1.1.4. The system registration shall collect the user's zip code.
- 1.1.1.5. The system shall allow users to register for email reminders.
- 1.1.1.6. The system shall allow users to reset their passwords.
- 1.1.1.7. The system shall allow users to login to their account.
- 1.1.1.8. The system shall allow users to logout of their account.

### 1.1.2 User De-Registration

- 1.1.2.1. The system shall allow the user to delete an account.
- 1.1.2.2. The system shall allow the user to de-register for email reminders.
- 1.2.1.3. The UI shall support Edge, Chrome, and Firefox.

### 1.1.3 Optimal Green Option Display

- 1.1.3.1. The system shall display providers with Fixed Price.
- 1.1.3.2. The system shall display providers with no cancellation fees.
- 1.1.3.3. The system shall display providers with 100% renewable energy.
- 1.1.3.4. The system shall display providers with options that are cheaper or within .05 cents per kWh of the user's distributor's current rate.
- 1.1.3.5. The system shall display the contract length of each energy supplier.
- 1.1.3.6. The optimal green option display shall allow the user to search for offers within their zip code.
- 1.1.3.7. The system shall display a message to the user if the zip code entered on the search page is not a valid PA zip code.
- 1.1.3.8. The system shall display the offer results to the user when the zip code entered is valid and there is a distributor and rate schedule selected.
- 1.1.3.9. The system shall have the user select their distributor for the zip code entered, if there is only a single distributor for their zip code auto-select the distributor and proceed.
- 1.1.3.10. The system shall have the user select their rate schedule for the distributor selected, if there is only a single rate schedule for the distributor auto-select the rate schedule.
- 1.1.3.11. If the user is logged in, the system shall persist the zip-code, distributor selected, and rate schedule selected.
- 1.1.3.12. If the user is logged in and they do not have a zip code, distributor, and rate schedule selected prompt them to select each upon search request.
- 1.1.3.13. If the user is logged in and they do have a zip code, distributor, and rate schedule selected the system shall prompt the user if they'd like to reselect search options.
- 1.1.3.14. If the user declines the prompt to reselect search options, the system shall use the persisted search options to get the offer results.

### 1.1.4 Provider Selection & Decision Retention

- 1.1.4.1. The system shall allow users to select a provider.
- 1.1.4.2. The system shall save the selected decision in the application database.
- 1.1.4.3. The system shall redirect users to the provider’s website for sign-up in a new tab.
- 1.1.4.4. Upon user selection of an offer, the system shall cache the offer in the database for the user as a "possible selection"
- 1.1.4.5. Upon login, page refresh, or request of a new page from the server, if the user has has any "possible selections" cached, the system shall prompt the user to choose if they signed up for any of the possible selection.
- 1.1.4.6. The possible selections prompt shall allow the user to easily select a "No" or "Skip" option
- 1.1.4.7. Once the user has completed interacting with the possible selection prompt (either selects or chooses no), the possible selections shall be deleted from the cache.

### 1.1.5 Automated Email Scheduling

- 1.1.5.1. The system shall schedule a follow-up email one month before the contract ends.
- 1.1.5.2. The follow-up emails’ subject and content shall be written in a minimum and direct format to avoid being flagged as spam.
- 1.1.5.3. The system shall schedule a follow-up email two weeks before the contract ends.
- 1.1.5.4. The system shall schedule a follow-up email two days before the contract ends.
- 1.1.5.5. The system shall generate a follow-up email to include alternative green supplier choices, the best and cheapest of that day and time, and provide a link to the application to sign up for the next deal.
- 1.1.5.6. The system shall generate a follow-up email upon registration.
- 1.1.5.7 The system shall email a follow-up when a cheaper contract is avaliable within the users zip code.

### 1.1.6 Notifications for New Contracts

- 1.1.6.1. The system shall email users whenever a new contract option comes up in their zip code that is lower than the rate they are currently using.

### 1.1.7 Web Parsing

- 1.1.7.1. The web parser shall be capable of retrieving the distributors for a given zip code.
- 1.1.7.2. The web parser shall be capable of filtering offers based on monthly usage.
- 1.1.7.3. The web parser shall be capable of filtering offers based on "price structure" (e.g. "fixed").
- 1.1.7.4. The web parser shall be capable of filtering offers based on renewable energy percentage.
- 1.1.7.5. The web parser shall raise an HTTP Error if it does not receive a 200 response

### 1.1.8 User Profile

- 1.1.8.1. The system shall have a page that displays the user profile.
- 1.1.8.2. The system shall only display a profile settings link when the user is logged on and authenticated.
- 1.1.8.3. The system shall display the user's persisted search options (zip code, distributor, and rate schedule)
- 1.1.8.4. The system shall allow the user to reselect their search options from the user profile. If they choose to reselect, the system shall use the same prompts as the primary search routine to maintain a similar feel.
- 1.1.8.5. The system shall allow the user to update their contract end date.

### 1.1.9 Offer Results

- 1.1.9.1. The system shall have a results page that displays rates regardless of logged in status.
- 1.1.9.2. The system shall display additional contract related results when the user is logged in and authenticated.

## Non-Functional Requirements

---

The non-functional requirements will focus on the qualities and attributes of the application that will be used to drive design and push constraints onto the backlog.

### 1.2.1 User Interface

- 1.2.1.1. The system shall be responsive and compatible with various devices and screen sizes, including desktop computers, laptops, tablets, and mobile phones.
- 1.2.1.2. The UI elements shall adapt dynamically to different screen resolutions and orientations, providing an optimal user experience across devices.
- 1.2.1.3. The UI shall support Edge, Chrome, and Firefox.

### 1.2.2 Application Performance

- 1.2.2.1. The website shall load and display search results within 3 seconds, ensuring a seamless user experience and minimizing user frustration caused by long loading times.

### 1.2.3 Application Relability

- 1.2.3.1 The website shall meet or exceed a 99.9% uptime, including during version updates.

### 1.2.4 Application Security

- 1.2.4.1 The website shall continuously check for vulnerabilities in existing frameworks, libraries, and deployments.
- 1.2.4.2 The CI/CD pipeline shall continuously check for vulnerabilities in existing frameworks, libraries, and deployments.

### 1.2.5 Application Testability

- 1.2.5.1 The website shall require a minimum coverage of 90% upon deployment into a production environment.
- 1.2.5.2 The CI/CD pipeline shall continuously check for coverage to be maintained above 90% in order to merge into stable branches.

## Documentation Requirements

### 1.3.1 End-User Documentation

- 1.3.1.1. The end-user documentation shall include a product overview with a list of tools, frameworks, and services needed to run the system
- 1.3.1.2. The end-user documentation shall include deployment instructions which details instructions to download and install each tool and environment configuration.
- 1.3.1.3. The deployment instructions shall include screenshots to demonstrate all instructions.
- 1.3.1.4. The end-user documentation shall include an application features section
- 1.3.1.5. The application features section shall detail a list of all the application features by category and include a short description of each functionality.
- 1.3.1.6. The end-user documentation shall include a features instruction section.
- 1.3.1.7. The features instructions section shall include detailed instructions to execute each user story and use case.
- 1.3.1.8. The features instructions section shall include screenshots for each application features provided to demonstrate the step-by-step instructions to execute the functionality.
