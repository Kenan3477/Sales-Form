<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->
- [x] Verify that the copilot-instructions.md file in the .github directory is created.

- [x] Clarify Project Requirements
	Project requirements are clearly specified: Next.js TypeScript Sales Form Portal with Prisma, PostgreSQL, NextAuth

- [x] Scaffold the Project
	Ensure that the previous step has been marked as completed.
	Call project setup tool with projectType parameter.
	Run scaffolding command to create project files and folders.
	Use '.' as the working directory.
	If no appropriate projectType is available, search documentation using available tools.
	Otherwise, create the project structure manually using appropriate file creation tools.

- [x] Customize the Project
	Verify that all previous steps have been completed successfully and you have marked the step as completed.
	Develop a plan to modify codebase according to user requirements.
	Apply modifications using appropriate tools and user-provided references.
	Skip this step for "Hello World" projects.

- [x] Install Required Extensions
	No extensions required for this Next.js project

- [x] Compile the Project
	Verify that all previous steps have been completed.
	Install any missing dependencies.
	Run diagnostics and resolve any issues.
	Check for markdown files in project folder for relevant instructions on how to do this.

- [x] Create and Run Task
	Verify that all previous steps have been completed.
	Check https://code.visualstudio.com/docs/debugtest/tasks to determine if the project needs a task. If so, use the create_and_run_task to create and launch a task based on package.json, README.md, and project structure.
	Skip this step otherwise.
	 
- [x] Launch the Project
	Verify that all previous steps have been completed.
	Prompt user for debug mode, launch only if confirmed.
	 
- [x] Ensure Documentation is Complete
	Verify that all previous steps have been completed.
	Verify that README.md and the copilot-instructions.md file in the .github directory exists and contains current project information.
	Clean up the copilot-instructions.md file in the .github directory by removing all HTML comments.

## Sales Form Portal Project
This is a Next.js TypeScript application for sales agents to submit customer sales and admins to manage submissions.

## Key Features:
- Role-based authentication (agent, admin)
- Dynamic sales form with appliance and boiler cover sections
- Live total cost calculation
- Admin panel for managing sales and exporting CSV
- Configurable mandatory/optional fields
- Responsive design

## Tech Stack:
- Next.js 14 with App Router
- TypeScript
- Prisma ORM with PostgreSQL
- NextAuth for authentication
- Tailwind CSS for styling
- React Hook Form for form handling

## Setup Complete!
The Sales Form Portal is now ready for development. The development server is running at http://localhost:3000.

### Next Steps:
1. Set up your PostgreSQL database
2. Copy .env.example to .env and configure your database connection
3. Run `npm run db:push` to create the database schema
4. Run `npm run db:seed` to create default users and settings
5. Visit http://localhost:3000 to start using the application

### Demo Accounts:
- Admin: admin@salesportal.com / admin123
- Agent: agent@salesportal.com / agent123