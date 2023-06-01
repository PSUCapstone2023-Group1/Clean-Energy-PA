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

### 1.1.2 User De-Registration

- 1.1.2.1. The system shall allow the user to delete an account.
- 1.1.2.2. The system shall allow the user to de-register for email reminders.
- 1.2.1.3. The UI shall support Edge, Chrome, and Firefox.

### 1.1.3 Optimal Green Option Display

- 1.1.3.1. The system shall display providers with Fixed Price.
- 1.1.3.2. The system shall display providers with no cancellation fees.
- 1.1.3.3. The system shall display providers with 100% renewable energy.
- 1.1.3.4. The system shall display providers with options that are cheaper or within 5 cents of the current PECO rate.
- 1.1.3.5. The system shall display the contract length of each energy supplier.

### 1.1.4 Provider Selection & Decision Retention

- 1.1.4.1. The system shall allow users to select a provider.
- 1.1.4.2. The system shall save the selected decision in the application database.
- 1.1.4.3. The system shall redirect users to the provider’s website for sign-up in a new tab.

### 1.1.5 Automated Email Scheduling

- 1.1.5.1. The system shall schedule a follow-up email one month before the contract ends.
- 1.1.5.2. The follow-up emails’ subject and content shall be written in a minimum and direct format to avoid being flagged as spam.
- 1.1.5.3. The system shall schedule a follow-up email two weeks before the contract ends.
- 1.1.5.4. The system shall schedule a follow-up email two days before the contract ends.
- 1.1.5.5. The system shall generate a follow-up email to include alternative green supplier choices, the best and cheapest of that day and time, and provide a link to the application to sign up for the next deal.
- 1.1.5.6. The system shall generate a follow-up email upon registration.

### 1.1.6 Notifications for New Contracts

- 1.1.6.1. The system shall email users whenever a new contract option comes up in their zip code that is lower than the rate they are currently using.

### 1.1.7 Web Parsing

- 1.1.7.1. The system shall be capable of pulling data based on zip code.
- 1.1.7.2. The system shall be capable of pulling data based on monthly usage.
- 1.1.7.3. The system shall be capable of pulling data based on the “Fixed Price” selection.
- 1.1.7.4. The system shall be capable of pulling data based on “100% renewable energy”.

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