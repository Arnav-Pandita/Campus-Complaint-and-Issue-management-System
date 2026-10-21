SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
Campus Complaint & Issue Management System
Version: 1.0
Project Type: Web Application
Document Type: Software Requirements Specification
________________________________________
1. Introduction
1.1 Purpose
The purpose of this document is to define the functional and non-functional requirements of the Campus Complaint & Issue Management System. It describes the system's expected behaviour, user roles, complaint-handling workflow, privacy requirements, interfaces, data requirements, and acceptance criteria.
This document serves as a reference for designing, developing, testing, and evaluating the system.

1.2 Scope
The Campus Complaint & Issue Management System is a web-based platform that enables college students to submit campus-related complaints, track their progress, and view complaints reported by other students.
The system provides separate interfaces for students, department administrators, and a Super Admin. Students select the relevant department when submitting a complaint. Department administrators manage complaints assigned to their departments, while the Super Admin oversees the entire system.
Students can submit complaints using their names or anonymously. All registered students can view published complaints, including their descriptions and uploaded images after acknowledging the image privacy warning.
The system includes priority management with mandatory reasons, in-app notifications, complaint reopening requests, status history, and accountability dashboards.
The system covers the following five departments:
1.	Maintenance & Facilities
2.	IT & Network
3.	Academic Administration
4.	Library
5.	Canteen & Food Services
An Other option is available for complaints that do not fit these departments. Such complaints can be assigned to an appropriate department by the Super Admin.
Hostel administration is explicitly excluded from the scope of this project.

1.3 Intended Audience
This document is intended for:
•	Project team members responsible for development.
•	Faculty members evaluating the Software Engineering project.
•	Testers responsible for verifying system requirements.
•	College representatives reviewing the proposed system.

1.4 Definitions and Abbreviations
Term	Definition
SRS	Software Requirements Specification
Student	A registered user who can submit and track complaints
Department Admin	An administrator responsible for complaints assigned to one department
Super Admin	An administrator with system-wide oversight and department-management privileges
Anonymous Complaint	A complaint whose submitter's identity is hidden from students and administrators
Complaint Access Code	A private code used to access and track an anonymous complaint
Priority	The urgency level assigned by an administrator
Status History	A record of changes made to a complaint's status
Priority History	A record of priority assignments and changes, including reasons
Overdue Complaint	A complaint that has exceeded its configured resolution target

1.5 Document Conventions
Requirements are identified using unique identifiers such as FR-01 for functional requirements and NFR-01 for non-functional requirements. Each requirement is intended to be individually testable wherever practical.

1.6 References
This document follows the general structure and principles of IEEE-style Software Requirements Specifications.


2. Overall Description
2.1 Product Perspective
The system is a standalone web application that centralizes campus complaint submission and management. It replaces informal reporting methods with a common platform that records complaint details, ownership, priority, status changes, and resolution history.
The system has three primary user roles:
•	Student: Submits, views, and tracks complaints.
•	Department Admin: Manages complaints assigned to their department.
•	Super Admin: Oversees all departments, manages department administrator accounts, and reassigns complaints when required.
All registered students can view published complaints across all five departments. Complaint-management actions are restricted according to user roles and department permissions.

2.2 Product Functions
The system provides the following major functions:
•	Student registration and authentication.
•	Complaint submission with predefined categories and department selection.
•	Visible-name and anonymous complaint options.
•	Image attachment with a privacy warning.
•	Public complaint board with status and priority information.
•	Similar-complaint suggestions before submission.
•	Department-wise complaint management.
•	Priority assignment with a mandatory reason.
•	Complaint status updates and resolution recording.
•	Student requests for reopening resolved complaints.
•	In-app notifications.
•	Complaint deletion before processing begins.
•	Accountability dashboards and historical records.
•	Super Admin oversight, department administrator management, and complaint reassignment.

2.3 User Classes and Characteristics
User Class	Responsibilities
Student	Register, log in, submit complaints, select identity visibility and department, view complaints, track personal complaints, request reopening, and delete eligible complaints
Department Admin	Manage complaints assigned to their department, set priorities with reasons, update status, record resolutions, and handle reopening requests
Super Admin	Oversee all departments, manage department administrator accounts, reassign complaints, and view system-wide accountability information
The system enforces role-based access so that users cannot perform actions outside their permissions.

2.4 Operating Environment
The system operates as a web application accessible through modern desktop and mobile browsers. A server-side application and database store user accounts, complaint information, attachments, status histories, and related records.
The specific programming language, framework, database, and hosting environment are implementation decisions and are not prescribed by this SRS.

2.5 Design and Implementation Constraints
•	Only registered students may submit complaints.
•	Student registration uses a college email address or college ID.
•	Administrator accounts are created or authorized separately by the Super Admin.
•	Only the five specified departments are included in the current scope.
•	Students select the department when submitting a complaint.
•	Department administrators manage complaints assigned to their departments.
•	Anonymous complaints do not reveal the complainant's identity through ordinary application interfaces.
•	The system provides in-app notifications only.
•	Automated image redaction, AI-based complaint classification, and automated priority assignment are excluded.

2.6 Assumptions and Dependencies
•	The college can provide or approve the student registration identifiers.
•	A mechanism for validating college email addresses or IDs will be established during implementation.
•	Super Admin accounts will be provisioned securely.
•	Resolution targets for determining overdue complaints will be configurable and established before deployment.
•	Users will provide accurate complaint information and use the platform responsibly.
•	The system will have sufficient server storage for complaint attachments.
•	Actual anonymity depends on implementation, access controls, database design, and infrastructure practices.


3. External Interface Requirements
3.1 User Interface Requirements
Student Interface
The student interface shall provide:
•	Registration and login pages.
•	A dashboard displaying personal complaints and their statuses.
•	A complaint submission form.
•	Department and complaint-category selection.
•	Identity visibility selection: Visible or Anonymous.
•	Attachment upload with a privacy warning.
•	A public complaint board with filters.
•	Complaint details and status history.
•	Anonymous complaint tracking using a private access code.
•	Reopening request and eligible complaint deletion options.
Department Admin Interface
The Department Admin interface shall provide:
•	A dashboard displaying complaints assigned to the administrator's department.
•	Filters for status, category, priority, and overdue state.
•	Complaint details and attachment viewing.
•	Priority assignment and reason entry.
•	Status update and resolution forms.
•	Reopening request management.
•	Complaint history and accountability information.
Super Admin Interface
The Super Admin interface shall provide:
•	A system-wide dashboard across all five departments.
•	Department administrator account management.
•	Department-wise complaint overview.
•	Complaint reassignment functionality.
•	Cross-department status, overdue, and resolution-time reporting.
•	Access to complaint-management information without revealing anonymous complainants' identities.

3.2 Hardware Interfaces
No specialized hardware is required. Users need a device capable of accessing a modern web browser. The server requires sufficient computing and storage resources for the application, database, and uploaded attachments.

3.3 Software Interfaces
The system interacts with:
•	A database for persistent storage.
•	A web server or application server for handling requests.
•	File storage for uploaded complaint images.
•	A browser-based interface for all user roles.
Email, SMS, push notifications, and third-party identity providers are not required within the current scope.

3.4 Communication Interfaces
Communication between the browser and server shall use standard web protocols. HTTPS shall be used in deployment to protect data transmitted between the client and server.

3.5 Error Handling and Validation
•	Required fields shall be validated before submission.
•	Invalid login attempts shall produce a general error message without exposing sensitive account information.
•	Failed complaint submissions shall provide a clear explanation and allow the user to correct the input.
•	Unauthorized actions shall be rejected.
•	Invalid complaint access codes shall not reveal complaint information.
•	Attachment upload failures shall be communicated to the user.
•	Destructive actions, such as deleting a complaint, shall require confirmation.

4. Functional Requirements
4.1 Registration and Authentication
ID	Requirement
FR-01	The system shall allow students to register using their college email address or college ID and a password.
FR-02	The system shall validate registration fields and reject duplicate accounts based on the chosen unique college identifier.
FR-03	The system shall authenticate registered students before allowing complaint submission or personal complaint management.
FR-04	The system shall provide a separate, restricted login path for administrators.
FR-05	The system shall allow the Super Admin to create, authorize, activate, or deactivate department administrator accounts.
FR-06	The system shall enforce role-based permissions for students, department administrators, and the Super Admin.
FR-07	The system shall prevent unauthorized access to restricted complaint-management functions.
FR-08	The system shall securely store passwords using an appropriate password-hashing mechanism.

4.2 Complaint Submission
ID	Requirement
FR-09	The system shall allow authenticated students to submit complaints.
FR-10	The complaint form shall require a title, description, complaint category, and selected department.
FR-11	The system shall provide the five defined departments and an Other fallback option.
FR-12	The student shall select the department to which the complaint should be routed.
FR-13	The system shall not automatically route a complaint solely based on its category.
FR-14	The system shall allow students to select either Visible or Anonymous identity mode for each complaint.
FR-15	For a Visible complaint, the student's name shall be displayed to other students and authorized administrators.
FR-16	For an Anonymous complaint, the public author label shall be Anonymous, and the application shall not expose the submitter's identity to administrators through ordinary application interfaces.
FR-17	The system shall generate a unique complaint identifier for each successfully submitted complaint.
FR-18	The system shall generate a private complaint-access code for anonymous complaints and present it securely to the student.
FR-19	The system shall provide a warning before image upload explaining that uploaded images may be visible to all students and may contain personal or sensitive information.
FR-20	The system shall allow students to attach supported image files, subject to configured file type and size limits.
FR-21	The system shall require the student to acknowledge the image privacy warning before submitting images.
FR-22	The system shall display similar complaints before final submission when relevant matches can be identified.
FR-23	Similar-complaint suggestions shall not prevent the student from submitting a new complaint.
FR-24	The system shall record the submission date and initial status of each complaint.
FR-25	A newly submitted complaint shall receive the initial status Open.
FR-26	The system shall route a complaint to the administrator responsible for the selected department, or leave an Other complaint available for Super Admin assignment.

4.3 Public Complaint Board
ID	Requirement
FR-27	The system shall provide an authenticated public complaint board accessible to all registered students.
FR-28	The board shall display published complaints across all five departments.
FR-29	The board shall display the complaint title, description, category, department, submission date, current status, and assigned priority when available.
FR-30	The board shall display the submitter's name for Visible complaints and Anonymous for Anonymous complaints.
FR-31	The board shall display uploaded complaint images after the student has acknowledged the privacy warning.
FR-32	The public board shall not display passwords, private access codes, private account information, or internal administrative records.
FR-33	The system shall allow students to filter or search complaints using available fields such as department, category, status, and priority.
FR-34	The system shall not provide student commenting or public discussion functionality.

4.4 Complaint Tracking, Editing and Deletion
ID	Requirement
FR-35	The system shall allow students to view the status of their Visible complaints through their accounts.
FR-36	The system shall allow students to track Anonymous complaints using the complaint identifier and private access code.
FR-37	The system shall not require anonymous complaint tracking to reveal the student's identity to an administrator.
FR-38	The system shall allow a student to delete their own complaint only while it remains Open and processing has not begun.
FR-39	The system shall disable student deletion once the complaint has entered In Progress or any later processing state.
FR-40	The system shall request confirmation before deleting an eligible complaint.
FR-41	Following permitted deletion, the complaint shall be removed from the public board and ordinary student access.

4.5 Department Administration
ID	Requirement
FR-42	The system shall support Department Admin accounts for Maintenance & Facilities, IT & Network, Academic Administration, Library, and Canteen & Food Services.
FR-43	A Department Admin shall be able to view and manage complaints assigned to their own department.
FR-44	A Department Admin shall not be able to manage complaints assigned to another department unless separately authorized as Super Admin.
FR-45	A Department Admin shall be able to inspect complaint details, attachments, current status, priority, and history for complaints under their responsibility.
FR-46	A Department Admin shall be able to update complaint status in accordance with the defined status workflow.
FR-47	A Department Admin shall be able to record resolution details before marking a complaint Resolved.
FR-48	A Department Admin shall be able to handle reopening requests for complaints assigned to their department.
FR-49	The system shall keep a history of administrative actions affecting complaint status, priority, assignment, and resolution.

4.6 Super Admin and Department Assignment
ID	Requirement
FR-50	The Super Admin shall be able to view complaints across all departments.
FR-51	The Super Admin shall be able to create, authorize, deactivate, and manage Department Admin accounts.
FR-52	The Super Admin shall be able to reassign a complaint to another department when the selected department is incorrect or the complaint requires reassignment.
FR-53	The system shall require a reason for complaint reassignment.
FR-54	The system shall record the previous department, new department, responsible administrator, timestamp, and reassignment reason.
FR-55	Reassigned complaints shall become manageable by the Department Admin responsible for the new department.
FR-56	The Super Admin shall be able to view cross-department accountability information, including open, overdue, resolved, and closed complaint counts and resolution times.
FR-57	The Super Admin shall not be able to identify the submitter of an Anonymous complaint through ordinary application interfaces.

4.7 Priority Management
ID	Requirement
FR-58	The system shall allow an authorized administrator to assign Low, Medium, or High priority to a complaint.
FR-59	The system shall require a reason whenever a priority is first assigned or changed.
FR-60	The system shall record the previous priority, new priority, reason, responsible administrator, and timestamp.
FR-61	The system shall display the current priority on the public complaint board.
FR-62	The system shall allow authorized administrators to review priority history.
FR-63	The system shall not automatically assign or change priority using AI or an automated classification model.

4.8 Complaint Status and Resolution
ID	Requirement
FR-64	The system shall support the statuses Open, In Progress, Resolved, and Closed.
FR-65	A new complaint shall begin in the Open state.
FR-66	An authorized administrator shall be able to move a complaint from Open to In Progress when work begins.
FR-67	An authorized administrator shall provide resolution details before changing a complaint to Resolved.
FR-68	An authorized administrator shall be able to close a resolved complaint in accordance with the permitted workflow.
FR-69	The system shall record the previous status, new status, actor, timestamp, and reason where applicable for every status change.
FR-70	The system shall not allow arbitrary status transitions that violate the defined workflow.

4.9 Reopening Requests
ID	Requirement
FR-71	The system shall allow a student to request reopening when a complaint is Resolved or Closed and the issue remains unresolved or the resolution is unsatisfactory.
FR-72	The system shall require a reason for a reopening request.
FR-73	The appropriate Department Admin shall be able to approve or reject a reopening request.
FR-74	The system shall record the reopening request, reason, decision, administrator, timestamp, and decision details.
FR-75	An approved reopening request shall return the complaint to In Progress.
FR-76	A rejected reopening request shall leave the complaint in its existing status.
FR-77	The system shall notify the student of the reopening decision through in-app notifications or the anonymous complaint tracking mechanism.

4.10 In-App Notifications
ID	Requirement
FR-78	The system shall provide in-app notifications for relevant complaint events.
FR-79	Students shall be notified of significant status changes, resolution, and reopening decisions for their complaints.
FR-80	Department Admins shall receive or see notifications about relevant complaints and pending actions within their department.
FR-81	The Super Admin shall be able to see relevant system-wide administrative notifications, such as items awaiting assignment or overdue complaints.
FR-82	Notifications shall not reveal the identity of a student who submitted an Anonymous complaint.
FR-83	The system shall not require SMS, email, or external push notifications as part of the current scope.

4.11 Accountability Dashboard
ID	Requirement
FR-84	The system shall provide Department Admins with a dashboard for complaints assigned to their department.
FR-85	The Department Admin dashboard shall show complaint counts by status, including Open, In Progress, Resolved, and Closed.
FR-86	The Super Admin dashboard shall show corresponding counts across all departments and permit department-wise comparison.
FR-87	The dashboards shall display overdue complaint counts based on configured resolution targets.
FR-88	The dashboards shall provide complaint resolution-time information and status history.
FR-89	The system shall calculate overdue status using configurable resolution targets.
FR-90	The system shall preserve priority, status, and reassignment histories so that accountability information can be reviewed.

4.12 Data Protection and Administrative Controls
ID	Requirement
FR-91	The system shall protect private complaint access codes from public display and unauthorized access.
FR-92	The system shall restrict access to personal account information according to user role and complaint identity settings.
FR-93	The system shall not expose anonymous complainant identity through ordinary administrator dashboards, complaint histories, notifications, or exports.
FR-94	The system shall prevent Department Admins from modifying complaints outside their authorized department.
FR-95	The system shall maintain a record of department reassignment and priority changes, including mandatory reasons.
FR-96	The system shall validate uploaded files for permitted types and size limits and apply appropriate security controls before storage or display.


5. Non-Functional Requirements
ID	Requirement
NFR-01 — Performance	Under normal expected college usage, common pages and operations should respond within 3 seconds, excluding unusually large uploads or network delays.
NFR-02 — Usability	The interface shall use clear labels, consistent navigation, and understandable error messages.
NFR-03 — Accessibility	Forms, navigation, status indicators, and messages should be usable with common accessibility features and keyboard navigation.
NFR-04 — Security	The system shall enforce authentication, role-based authorization, secure password storage, input validation, and protection against common web vulnerabilities.
NFR-05 — Privacy	Personal information shall be exposed only where required by the selected identity setting and authorized system functions.
NFR-06 — Anonymity	Anonymous complaint identity shall be protected within the application's defined security boundary, including against access by Department Admins and the Super Admin through ordinary application interfaces.
NFR-07 — Data Integrity	Complaint identifiers, status histories, priority histories, and assignment records shall remain consistent when complaints are updated or reassigned.
NFR-08 — Reliability	The system should handle expected concurrent users without losing successfully recorded complaint submissions or administrative changes.
NFR-09 — Maintainability	The application should be organized into understandable modules so that authentication, complaint handling, notifications, and administration can be maintained separately.
NFR-10 — Compatibility	The application should work on recent versions of commonly used desktop and mobile browsers.
NFR-11 — Auditability	Priority changes, status changes, and department reassignments shall have sufficient history to establish what changed, when, and by whom.
NFR-12 — Storage Security	Uploaded images and complaint records shall be protected against unauthorized modification, disclosure, and access.
NFR-13 — Scalability	The design should permit additional complaints and users to be accommodated through reasonable changes to server and database resources.
NFR-14 — Data Validation	The application shall validate required fields, text lengths, attachment types, and attachment sizes before accepting data.
NFR-15 — Deployment Security	The deployed system shall use HTTPS and appropriate session-management protections.

6. Use Cases
6.1 Use Case UC-01: Student Registration and Login
Primary Actor: Student
Preconditions:
•	The student has a valid college email address or college ID.
•	The student has access to the application.
Main Flow:
1.	The student opens the registration page.
2.	The student enters the required college identifier and password.
3.	The system validates the input and checks for duplicate accounts.
4.	The system applies the configured registration-verification procedure.
5.	The account is created, and the student can log in.
Alternative Flows:
•	Invalid or duplicate registration information is rejected with an explanatory message.
•	Incorrect login credentials are rejected without revealing sensitive account details.
Postcondition: The student can access permitted student functions after successful authentication.

6.2 Use Case UC-02: Submit a Complaint
Primary Actor: Student
Preconditions:
•	The student is authenticated.
•	The complaint form is available.
Main Flow:
1.	The student opens the complaint submission form.
2.	The student enters a title, description, category, and selected department.
3.	The student selects Visible or Anonymous identity mode.
4.	The system may display similar complaints.
5.	If the student attaches images, the system displays the privacy warning and obtains acknowledgement.
6.	The student submits the complaint.
7.	The system validates the information, creates a complaint identifier, and sets the status to Open.
8.	The system routes the complaint to the selected department or makes an Other complaint available for Super Admin assignment.
9.	For an Anonymous complaint, the system securely provides a private access code.
Alternative Flows:
•	Missing or invalid fields are highlighted.
•	The student may proceed despite similar-complaint suggestions.
•	If an upload or submission fails, the system displays an error and does not falsely report success.
Postcondition: A valid complaint is recorded and becomes available according to the system's visibility rules.

6.3 Use Case UC-03: Manage a Department Complaint
Primary Actor: Department Admin
Preconditions:
•	The administrator is authenticated.
•	The complaint is assigned to that administrator's department.
Main Flow:
1.	The administrator opens the department dashboard.
2.	The administrator selects a complaint.
3.	The administrator reviews the complaint details and relevant history.
4.	The administrator assigns or changes priority and provides a reason.
5.	The administrator changes the status when work begins.
6.	The administrator records resolution details before marking the complaint Resolved.
7.	The system records the relevant histories and creates appropriate in-app notifications.
Alternative Flows:
•	The administrator cannot manage a complaint assigned to another department.
•	An invalid status transition is rejected.
•	A priority change without a reason is rejected.
Postcondition: The complaint and its history reflect the permitted administrative actions.

6.4 Use Case UC-04: Reassign a Complaint
Primary Actor: Super Admin
Preconditions:
•	The Super Admin is authenticated.
•	The complaint requires reassignment.
Main Flow:
1.	The Super Admin opens the system-wide dashboard.
2.	The Super Admin selects the complaint.
3.	The Super Admin selects a new department.
4.	The Super Admin enters a reassignment reason.
5.	The system updates the assignment and records the previous department, new department, actor, reason, and timestamp.
6.	The complaint becomes manageable by the new department's administrator.
Postcondition: The complaint is assigned to the appropriate department with an auditable reassignment record.

6.5 Use Case UC-05: Track an Anonymous Complaint
Primary Actor: Student who submitted an Anonymous complaint
Preconditions:
•	An Anonymous complaint has been submitted.
•	The student has the complaint identifier and private access code.
Main Flow:
1.	The student opens the anonymous tracking page.
2.	The student enters the complaint identifier and access code.
3.	The system validates the credentials.
4.	The system displays the complaint's status, relevant history, and available tracking actions without requiring disclosure of the student's identity to administrators.
5.	The student can submit a reopening request when eligible.
Alternative Flow: Invalid credentials are rejected without disclosing the complaint's private information.
Postcondition: The student can track the complaint without making their identity publicly visible.

6.6 Use Case UC-06: Request Reopening
Primary Actor: Student
Secondary Actor: Department Admin
Preconditions:
•	The complaint is Resolved or Closed.
•	The student believes the issue remains unresolved or the resolution is unsatisfactory.
Main Flow:
1.	The student opens the complaint tracking page.
2.	The student submits a reopening request with a reason.
3.	The relevant Department Admin reviews the request.
4.	The administrator approves or rejects it.
5.	If approved, the complaint returns to In Progress.
6.	The system records the decision and notifies the student through the permitted notification or tracking mechanism.
Postcondition: The reopening decision and its history are recorded.

6.7 Use Case UC-07: Review Accountability Dashboard
Primary Actors: Department Admin and Super Admin
Main Flow:
1.	The administrator opens the dashboard.
2.	The system displays counts by status, overdue complaint counts, and resolution-time information.
3.	A Department Admin views the data for their own department.
4.	The Super Admin can view and compare information across all departments.
5.	The administrator can review individual complaint histories where authorized.
Postcondition: The administrator can review complaint progress and identify unresolved or overdue cases.


7. Data Requirements
7.1 Main Data Entities
Entity	Important Attributes	Purpose
User	User ID, college identifier, password hash, role, account status	Stores student and administrator accounts
Department	Department ID, department name, assigned administrator	Defines the five supported departments and their administrators
Complaint	Complaint ID, title, description, category, department, identity mode, status, priority, submission date	Stores the main complaint record
Attachment	Attachment ID, complaint ID, storage reference, file type, size, upload date	Stores metadata for complaint images
Priority History	Complaint ID, old priority, new priority, reason, actor, timestamp	Records priority assignment and changes
Status History	Complaint ID, old status, new status, actor, timestamp, reason	Records the complaint lifecycle
Reassignment History	Complaint ID, old department, new department, actor, reason, timestamp	Records complaint reassignment
Reopening Request	Request ID, complaint ID, reason, decision, reviewer, timestamp	Stores reopening requests and decisions
Notification	Notification ID, recipient, event, message, creation time, read status	Stores in-app notifications
Anonymous Access Credential	Complaint ID, protected credential representation, creation and revocation information	Supports secure anonymous complaint tracking

7.2 Data Validation Rules
•	Each complaint shall have a unique complaint identifier.
•	Every complaint shall reference a valid department or an unassigned state awaiting Super Admin routing.
•	Complaint status and priority shall use the defined permitted values.
•	Priority changes shall include a reason.
•	Department reassignments shall include a reason.
•	Reopening requests shall include a reason.
•	Attachment type and size shall be validated before acceptance.
•	A complaint shall not be marked Resolved without resolution details.
•	Anonymous access credentials shall not be included in public complaint data or ordinary administrative records.
•	Only authorized users shall be able to modify protected records.

7.3 Data Retention and Deletion
The system shall support deletion of a student's complaint only before processing begins, as defined in the functional requirements. The implementation shall define how associated attachments and derived records are handled after deletion.
The system shall preserve relevant priority and status histories for complaints that have entered processing. Any retention or deletion policy required by the college shall be established before deployment.

7.4 Data Privacy
•	Public complaint data shall be separated from private authentication and tracking information.
•	Anonymous complaint access codes shall be protected and shall not be stored in a directly readable form where avoidable.
•	Anonymous complaint records shall not expose student identity through normal application queries, dashboards, exports, or notifications.
•	Uploaded images shall be displayed according to the public visibility policy and the student's acknowledgement of the privacy warning.
•	The application shall not claim to automatically detect or remove sensitive information from images.


8. Business Rules
ID	Business Rule
BR-01	Only authenticated students can submit complaints.
BR-02	A student must select a department when submitting a complaint.
BR-03	Only five departments are included in the current scope: Maintenance & Facilities, IT & Network, Academic Administration, Library, and Canteen & Food Services.
BR-04	Other is a fallback selection and not a sixth department; the Super Admin may assign it to an appropriate department.
BR-05	All registered students can view published complaints across departments.
BR-06	Each complaint has its own identity setting: Visible or Anonymous.
BR-07	Anonymous complainant identity shall be hidden from students and administrators through ordinary application interfaces.
BR-08	Anonymous complaints require private access credentials for complaint tracking.
BR-09	The student must acknowledge the image privacy warning before submitting images.
BR-10	Similar-complaint suggestions shall never prevent a new complaint submission.
BR-11	Students cannot comment on complaints.
BR-12	Students can delete their own complaints only before processing begins.
BR-13	Department Admins may manage only complaints assigned to their department.
BR-14	The Super Admin can oversee all departments and reassign complaints with a recorded reason.
BR-15	Priority can be assigned or changed only by an authorized administrator, and every assignment or change requires a reason.
BR-16	Every complaint begins in Open status.
BR-17	Resolution details are mandatory before a complaint can be marked Resolved.
BR-18	Students may request reopening of Resolved or Closed complaints; an administrator must decide the request.
BR-19	Approved reopening returns the complaint to In Progress.
BR-20	In-app notifications are the only notification channel required in the current scope.
BR-21	The system shall not use AI to assign complaint categories, priority, or identity visibility.
BR-22	Hostel administration and hostel-specific workflows are excluded from the current project.

9. Acceptance Criteria
ID	Acceptance Criterion	Verification Method
AC-01	A student can register and log in using valid credentials.	Functional test
AC-02	Invalid registration data and duplicate college identifiers are rejected.	Functional test
AC-03	A student can submit a complaint with all required fields and select one of the five departments or Other.	Functional test
AC-04	A complaint is assigned to the selected department, while an Other complaint can be assigned by the Super Admin.	Integration test
AC-05	A Visible complaint displays the student's name, while an Anonymous complaint displays Anonymous.	Functional and privacy test
AC-06	Anonymous complaint tracking works with the correct complaint identifier and access code; invalid credentials do not expose complaint information.	Security test
AC-07	The image warning must be acknowledged before image submission, and uploaded images are visible according to the defined public visibility rules.	Functional test
AC-08	Similar-complaint suggestions appear when applicable but do not block submission.	Functional test
AC-09	Department Admins cannot manage complaints assigned to another department.	Authorization test
AC-10	The Super Admin can view complaints across departments and reassign a complaint with a mandatory reason.	Functional test
AC-11	A priority cannot be assigned or changed without a reason, and its history is recorded.	Functional test
AC-12	Status transitions follow the defined workflow, and resolution details are required before marking a complaint Resolved.	Functional test
AC-13	A student can delete a complaint before processing begins but cannot delete it after it enters In Progress.	Functional test
AC-14	A reopening request can be approved or rejected, and an approved request returns the complaint to In Progress.	Functional test
AC-15	Relevant users receive in-app notifications for specified complaint events.	Integration test
AC-16	Department and system-wide dashboards display the correct status counts, overdue counts, and resolution-time information.	Data validation test
AC-17	Students cannot comment on complaints, and no hostel-specific administration workflow is available.	Functional test
AC-18	Public pages, dashboards, and notifications do not expose anonymous complainants' identities or private access codes.	Security and privacy test
AC-19	The application meets the agreed performance target under a representative test workload.	Performance test
AC-20	Common browser workflows work on supported desktop and mobile browsers.	Compatibility test


10. Verification and Traceability
10.1 Verification Approach
The project shall use the following verification methods:
•	Unit Testing: Verify individual functions such as validation, priority updates, and status transitions.
•	Integration Testing: Verify interactions between authentication, complaint storage, notifications, department routing, and dashboards.
•	System Testing: Test complete student and administrator workflows.
•	Security Testing: Test authorization boundaries, access-code protection, file-upload controls, and privacy restrictions.
•	Usability Testing: Check whether students and administrators can complete common tasks without unnecessary confusion.
•	Acceptance Testing: Compare the implemented application with the acceptance criteria in Section 9.

10.2 Requirements Traceability Matrix
Requirement Area	Requirement IDs	Related Acceptance Criteria
Registration and authentication	FR-01–FR-08	AC-01, AC-02
Complaint submission and routing	FR-09–FR-26	AC-03, AC-04, AC-07, AC-08
Public complaint board	FR-27–FR-34	AC-05, AC-07, AC-17
Tracking and deletion	FR-35–FR-41	AC-06, AC-13
Department administration	FR-42–FR-49	AC-09, AC-12
Super Admin and reassignment	FR-50–FR-57	AC-10, AC-18
Priority management	FR-58–FR-63	AC-11
Status and resolution	FR-64–FR-70	AC-12
Reopening requests	FR-71–FR-77	AC-14
Notifications	FR-78–FR-83	AC-15
Accountability dashboards	FR-84–FR-90	AC-16
Data protection	FR-91–FR-96	AC-06, AC-18
Non-functional requirements	NFR-01–NFR-15	AC-18–AC-20, as applicable


11. Known Limitations and Implementation Notes
11.1 Anonymity Limitations
Anonymous complaints must remain anonymous to students and administrators through the application's ordinary interfaces. Achieving this requires deliberate design; merely hiding the student's name on the public board is insufficient.
The implementation should protect access credentials, restrict database permissions, and prevent identity leakage through logs, exports, notifications, and administrative dashboards.
However, the application cannot promise absolute anonymity against every infrastructure-level observation, such as privileged server access, network records, or compromised devices. The system therefore provides application-level anonymity rather than immunity from every possible external or infrastructure-level investigation.

11.2 Public Image Privacy
Uploaded images may reveal faces, phone numbers, student IDs, or other sensitive details. The system displays a privacy warning and requires acknowledgement, but automated detection or redaction is outside the current scope. Users are responsible for checking their images before uploading them.

11.3 Priority Fairness
Requiring a reason for every priority assignment or change improves traceability but does not guarantee that all administrators will make fair decisions. Priority history and dashboards allow the Super Admin to review decisions and identify potential inconsistencies.

11.4 Department Routing
Students select the department themselves. The Super Admin can reassign incorrectly routed complaints, and the reassignment history records the reason and responsible administrator. Automatic category-based routing is not required.

11.5 Overdue Complaints
The application requires resolution targets to determine when a complaint becomes overdue. These targets must be configured before deployment. This SRS does not assume a specific number of hours or days for every complaint.

11.6 Scope Limitations
The current release excludes:
•	Hostel administration and hostel-specific complaint workflows.
•	Student comments or discussion threads.
•	Automated AI-based complaint classification or priority assignment.
•	Automated face detection, text detection, or image redaction.
•	SMS, email, or external push notifications.
•	Complex automatic escalation policies.
•	Public performance rankings of individual administrators.
These features may be considered in future versions but are not required for acceptance of the current project.


12. Future Enhancements
The following enhancements may be considered after the core system has been implemented and tested:
•	Integration with an official college identity or single sign-on system.
•	Configurable escalation rules for overdue complaints.
•	Advanced reporting and trend analysis.
•	Accessibility improvements based on user testing.
•	Additional departments following approval and requirements analysis.
•	Advanced duplicate detection beyond basic similar-complaint suggestions.
These are optional future enhancements and shall not expand the current implementation scope without approval.


13. Conclusion
The Campus Complaint & Issue Management System provides a centralized platform for submitting, tracking, and managing campus complaints. Its three-role structure—Student, Department Admin, and Super Admin—supports department-wise responsibility while maintaining a public complaint board accessible to all registered students.
The system combines anonymous complaint submission, private tracking, mandatory priority reasons, complaint history, reopening requests, in-app notifications, and accountability dashboards. The selected scope deliberately excludes hostel administration and other advanced features to keep the project feasible for a college-level Software Engineering course.
The requirements and acceptance criteria in this document provide the basis for system design, implementation, testing, and project evaluation.

