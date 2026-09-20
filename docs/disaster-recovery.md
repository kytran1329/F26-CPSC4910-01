# Disaster Recovery Plan

## Good (Truck) Driver Incentive Program

**Course:** CPSC 4910 — Fall 2026  
**Repository:** `F26-CPSC4910-01`  
**Document Version:** 1.0  
**Last Updated:** September 2026

---

## 1. Purpose

The purpose of this disaster recovery plan is to provide a well-documented procedure for recovering the Good (Truck) Driver Incentive Program application after a system failure, data loss, configuration loss, or other disaster.

The goal is to allow the development team to restore the application in a consistent and organized manner while minimizing data loss and application downtime.

---

## 2. Scope

This plan covers recovery of the major components of the application:

- Flask web application
- EC2 application server
- MySQL RDS database
- Application source code
- Environment configuration
- Application dependencies
- Database backups and snapshots

The plan focuses on the current development architecture and can be updated as the project moves toward production.

---

## 3. Current System Architecture

The current application uses the following technologies and AWS resources:

| Component | Current Configuration |
|---|---|
| Programming Language | Python |
| Web Framework | Flask |
| Source Control | GitHub |
| Repository | `F26-CPSC4910-01` |
| Application Hosting | AWS EC2 |
| EC2 Instance | `t3.micro` |
| Operating System | Amazon Linux |
| Application Deployment | Manual |
| Application Startup | `python app.py` |
| Application Access | EC2 public IP |
| Database | MySQL |
| MySQL Version | 8.4.11 |
| Database Hosting | AWS RDS |
| RDS Instance | `db.t3.small` |
| Database Port | 3306 |
| RDS Availability | Single-AZ |
| Automated Backup Retention | 7 days |
| Cross-Region Replication | None |
| Manual Snapshot | `cpsc4910-team01-snapshot` |

The current application is still in development, so deployment and recovery procedures are primarily manual.

---

## 4. Components That Require Recovery

The following components may need to be recovered after a disaster:

| Component | Recovery Method |
|---|---|
| EC2 instance | Create replacement EC2 instance |
| Flask application | Clone repository from GitHub |
| Python environment | Install Python and application dependencies |
| MySQL database | RDS automated backup, point-in-time recovery, or manual snapshot |
| `.env` configuration | Recreate using documented variable names and configuration |
| Application code | GitHub repository |
| Dependencies | `requirements.txt` |
| Database connection | Recreate `.env` configuration |
| Application access | Obtain replacement EC2 public IP |

---

## 5. Disaster Scenarios

The disaster recovery procedure is designed to address the following scenarios.

### 5.1 EC2 Failure

The EC2 instance may become unavailable, crash, or otherwise become unusable.

**Recovery approach:**

Create a replacement EC2 instance, install the required software, clone the GitHub repository, recreate the environment configuration, and restart the Flask application.

### 5.2 RDS Failure

The MySQL database may become unavailable or experience a failure.

**Recovery approach:**

Determine whether the database can be brought back online normally. If recovery is necessary, restore the database using an RDS automated backup, point-in-time recovery, or an appropriate manual snapshot.

### 5.3 Accidental Data Deletion or Corruption

Data may be accidentally deleted or changed incorrectly.

**Recovery approach:**

Use the RDS automated backup and point-in-time recovery capabilities when appropriate. A manual snapshot can also be used when a known-good snapshot exists.

### 5.4 Bad Code Deployment

A code change may cause the application to stop working or introduce unexpected behavior.

**Recovery approach:**

Identify the problematic change, use GitHub to return to a known-good version of the code, redeploy the application, and test the application.

### 5.5 Lost Configuration

The `.env` file or other server configuration may be lost.

**Recovery approach:**

Recreate the configuration using the documented environment variable names and the appropriate database connection information. Actual secrets must never be stored in the repository.

---

## 6. Recovery Objectives

### Recovery Point Objective (RPO)

**Target RPO: 24 hours**

The project has selected a 24-hour RPO because the application is currently in development and does not require production-level continuous replication.

The RPO represents the target amount of data loss the team is prepared to accept during recovery.

The actual available recovery point depends on the AWS RDS backup and restore capabilities at the time of the incident.

### Recovery Time Objective (RTO)

**Target RTO: 8 hours**

The project has selected an 8-hour RTO because the current recovery process is primarily manual.

Recovery may require:

1. Creating a replacement EC2 instance.
2. Installing Python.
3. Installing application dependencies.
4. Cloning the GitHub repository.
5. Recreating the `.env` configuration.
6. Connecting the application to RDS.
7. Starting the Flask application.
8. Testing the application.

The team will use 8 hours as the target time to restore the application to a usable state.

---

## 7. Database Backup Strategy

The MySQL database is hosted using AWS RDS.

### Current Backup Configuration

- Database: MySQL 8.4.11
- RDS instance: `db.t3.small`
- Port: 3306
- Availability: Single-AZ
- Automated backups: Enabled
- Automated backup retention: 7 days
- Backup target: AWS Cloud
- Backup region: US East (N. Virginia)
- Cross-region replication: Not currently configured
- Manual snapshot: `cpsc4910-team01-snapshot`
- Manual snapshot encryption: KMS encrypted

### Backup Requirements

The team should:

- Keep automated RDS backups enabled.
- Use automated backups for recent recovery needs.
- Use point-in-time recovery when appropriate for accidental deletion or corruption.
- Create a manual RDS snapshot before major or high-risk database changes.
- Verify that backups and snapshots are available.
- Document which backup or snapshot was used during a recovery.
- Record any data loss that occurred during recovery.

### Current Backup Strategy

The current project does not require Multi-AZ or cross-region database replication.

These capabilities may be considered future improvements if the application's availability requirements increase.

---

## 8. Application and Code Recovery

The application source code is maintained in GitHub.

The repository contains the application code and supporting files, including:

- `app.py`
- `requirements.txt`
- `.env.example`
- `SQL/`
- `static/`
- `templates/`

The `.env` file is not stored in GitHub.

If the EC2 instance is lost, the application can be recovered from the GitHub repository.

### General Application Recovery Process

1. Create or recover an EC2 instance.
2. Install Python.
3. Install the application's required dependencies.
4. Clone the GitHub repository.
5. Recreate the `.env` file.
6. Configure the application to connect to the RDS database.
7. Start the application using:

```bash
python app.py
```

8. Obtain the EC2 public IP address.
9. Access the application through the public IP.
10. Test the application and database connection.

---

## 9. Configuration and Secrets

The application uses an `.env` file for database configuration.

The known environment variable names are:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

Actual values for these variables must not be stored in the GitHub repository or in this disaster recovery document.

The `.env.example` file can be used to document the required variable names without exposing secrets.

### Security Requirements

The team must not commit the following information to GitHub:

- Database passwords
- AWS access keys
- AWS secret keys
- GitHub tokens
- Actual `.env` values
- Other application credentials
- Private keys

If configuration is lost during a disaster, the `.env` file must be recreated manually using the appropriate secure values.

---

## 10. EC2 Recovery Procedure

If the EC2 instance becomes unavailable, use the following procedure.

### Step 1: Identify the Failure

Confirm that the application server is unavailable and determine whether the issue is isolated to EC2.

### Step 2: Verify Database Availability

Check the RDS instance.

If the database is still available and functioning correctly, continue with application recovery.

If the database is unavailable, follow the RDS recovery procedure in Section 11.

### Step 3: Create a Replacement EC2 Instance

Create a replacement EC2 instance using the appropriate project configuration.

The current application server uses:

- `t3.micro`
- Amazon Linux

### Step 4: Install Python

Install Python on the replacement EC2 instance.

### Step 5: Install Application Dependencies

Install the dependencies required by the application.

The project's `requirements.txt` file should be used to identify the application's Python dependencies.

### Step 6: Clone the GitHub Repository

Clone the project repository onto the replacement EC2 instance.

The repository is:

```text
F26-CPSC4910-01
```

### Step 7: Recreate the `.env` File

Create the `.env` file on the EC2 instance using the required environment variable names.

Do not commit the `.env` file to GitHub.

### Step 8: Configure Database Connection

Verify that the application is configured to connect to the correct RDS database.

### Step 9: Start Flask

Start the application using:

```bash
python app.py
```

### Step 10: Access the Application

Obtain the public IP address of the replacement EC2 instance and use it to access the application.

### Step 11: Test the Application

Verify that:

- The webpage loads.
- Flask starts successfully.
- The application can connect to MySQL.
- Expected data displays.
- Important application functionality works.

### Step 12: Confirm Recovery

If possible, have a second team member verify that the application is functioning correctly.

Record the recovery details and any issues encountered.

---

## 11. RDS Recovery Procedure

If the MySQL RDS database becomes unavailable or data is lost, determine the appropriate recovery method.

### Option 1: Restore From Automated Backup

Use an available RDS automated backup when the required recovery point is within the automated backup retention period.

The current automated backup retention period is 7 days.

### Option 2: Point-in-Time Recovery

Use point-in-time recovery when the team needs to recover the database to a specific available point in time.

This is particularly useful for accidental data deletion or corruption.

### Option 3: Restore From Manual Snapshot

Use the manual snapshot when an appropriate known-good snapshot is available.

The current documented manual snapshot is:

```text
cpsc4910-team01-snapshot
```

The snapshot is KMS encrypted.

### After Database Recovery

After restoring the database:

1. Verify that the RDS instance is available.
2. Verify the MySQL database.
3. Verify that expected tables and data are present.
4. Confirm database connection information.
5. Update the application configuration if necessary.
6. Start or restart the Flask application.
7. Test database-dependent functionality.

---

## 12. Bad Deployment Recovery

If a deployment causes the application to stop working:

1. Identify the change that caused the issue.
2. Review the recent GitHub commits.
3. Identify the most recent known-good version.
4. Return the working copy to the known-good version.
5. Restart the Flask application.
6. Test the application.
7. Confirm that the issue has been resolved.
8. Document the failed deployment and recovery.

The exact Git workflow may change as the team's deployment process becomes more automated.

---

## 13. Lost Configuration Recovery

If the `.env` file is lost:

1. Create a new `.env` file.
2. Add the required environment variables:

```text
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

3. Enter the appropriate secure values.
4. Verify that the application can connect to RDS.
5. Start the Flask application.
6. Test database functionality.

Actual credentials should be obtained through the team's secure process and must not be placed in GitHub.

---

## 14. Recovery Prerequisites

The following resources and access should be available before recovery begins.

### AWS

- AWS account access
- Permission to manage EC2
- Permission to manage RDS
- Permission to restore RDS backups or snapshots
- Access to the project's AWS resources

### GitHub

- Access to the `F26-CPSC4910-01` repository
- Ability to clone the repository
- Ability to access the appropriate project branch

### Application Information

- Python installation instructions
- Application dependency information
- `.env` variable names
- RDS connection information
- EC2 configuration information

### Recovery Documentation

- This disaster recovery plan
- Disaster recovery checklist
- RDS backup information
- Manual snapshot information

---

## 15. Team Responsibilities

The team should establish specific recovery responsibilities as the project develops.

During a disaster, the team should:

1. Identify the affected component.
2. Determine the appropriate recovery procedure.
3. Assign a team member to perform the recovery.
4. Have another team member verify the recovered system when possible.
5. Record the recovery process.
6. Record any data loss.
7. Record the recovery time.
8. Identify improvements that should be made to the recovery process.

Team members should ensure that recovery information remains up to date as the application architecture changes.

---

# 16. Disaster Recovery Checklist

## Before Recovery

- [ ] Identify the type of failure.
- [ ] Determine which system component is affected.
- [ ] Confirm AWS access.
- [ ] Confirm GitHub access.
- [ ] Check RDS availability.
- [ ] Identify the latest usable backup or snapshot.
- [ ] Determine whether data recovery is necessary.

## Database Recovery

- [ ] Determine whether the existing RDS instance can be used.
- [ ] Identify the appropriate automated backup or recovery point.
- [ ] Restore the RDS database if necessary.
- [ ] Use point-in-time recovery if appropriate.
- [ ] Use the manual snapshot if appropriate.
- [ ] Verify that MySQL is available.
- [ ] Verify expected tables and data.
- [ ] Confirm database connection information.

## EC2 Recovery

- [ ] Create a replacement EC2 instance if necessary.
- [ ] Configure the instance appropriately.
- [ ] Install Python.
- [ ] Install application dependencies.
- [ ] Clone the GitHub repository.
- [ ] Recreate the `.env` file.
- [ ] Configure the database connection.
- [ ] Start the Flask application.
- [ ] Obtain the EC2 public IP address.
- [ ] Access the application.

## Application Verification

- [ ] Verify that the webpage loads.
- [ ] Verify that Flask starts successfully.
- [ ] Verify that the application can connect to MySQL.
- [ ] Verify that expected data displays.
- [ ] Test important application functionality.
- [ ] Have another team member verify the application if possible.

## After Recovery

- [ ] Record the recovery date and time.
- [ ] Record the disaster or failure.
- [ ] Record the backup or snapshot used.
- [ ] Record any data loss.
- [ ] Record the total recovery time.
- [ ] Determine whether the 24-hour RPO was met.
- [ ] Determine whether the 8-hour RTO was met.
- [ ] Document any problems encountered.
- [ ] Identify improvements to the recovery process.
- [ ] Update this disaster recovery plan if necessary.

---

## 17. Recovery Testing

The disaster recovery procedure should be tested periodically to ensure that the documented steps are accurate.

Testing should verify that the team can:

- Create a replacement EC2 instance.
- Install Python and application dependencies.
- Clone the application from GitHub.
- Recreate the `.env` configuration.
- Connect the application to RDS.
- Restore an RDS backup or snapshot when appropriate.
- Start the Flask application.
- Access the application.
- Verify important functionality.

Testing should be performed without exposing or using unnecessary production credentials.

The team should document the results of recovery tests and update this plan when the procedure changes.

---

## 18. Current Limitations

The current disaster recovery strategy has several limitations:

- Application deployment is manual.
- The application currently relies on a single EC2 instance.
- The RDS database is Single-AZ.
- Cross-region database replication is not configured.
- The `.env` file must currently be recreated manually.
- Exact EC2 security group configuration still needs to be fully documented.
- The exact Python version used on the EC2 instance should be documented.
- The full EC2 setup process should be verified against `requirements.txt`.
- Automated deployment has not yet been finalized.
- Infrastructure-as-code has not yet been implemented.

These limitations should be addressed as the project becomes more mature.

---

## 19. Future Improvements

Potential future improvements include:

- Automating application deployment.
- Using infrastructure-as-code to recreate AWS resources.
- Using a secure secrets management system.
- Adding application and infrastructure monitoring.
- Performing regular disaster recovery tests.
- Documenting EC2 security groups and network configuration.
- Documenting the exact Python version and installation process.
- Adding automated deployment rollback.
- Evaluating Multi-AZ RDS.
- Evaluating cross-region database recovery.
- Improving application availability.
- Automating portions of the recovery checklist.

These improvements are not currently required for the project's basic recovery procedure but could reduce recovery time and manual effort.

---

## 20. Document Maintenance

This document should be updated whenever the application's infrastructure, deployment process, database configuration, or recovery process changes.

The team should review the document after:

- Major architecture changes.
- Changes to AWS resources.
- Changes to the database.
- Changes to the deployment process.
- Disaster recovery tests.
- Actual recovery incidents.

The GitHub repository should contain the maintained Markdown version of this document.

The document should never contain passwords, API keys, AWS credentials, GitHub tokens, or other secrets.

---

## 21. Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | Fall 2026 | Initial disaster recovery plan created |

---

# 22. Quick Recovery Summary

The overall recovery process is:

```text
Identify failure
        ↓
Determine affected component
        ↓
Restore RDS if necessary
        ↓
Create replacement EC2
        ↓
Install Python and dependencies
        ↓
Clone GitHub repository
        ↓
Recreate .env
        ↓
Start Flask
        ↓
Access public IP
        ↓
Test application
        ↓
Confirm recovery
        ↓
Document incident
```

### Recovery Targets

**RPO:** 24 hours

**RTO:** 8 hours

### Primary Recovery Resources

- GitHub repository: `F26-CPSC4910-01`
- Application: Python/Flask
- Application server: AWS EC2 `t3.micro`
- Database: AWS RDS MySQL 8.4.11
- Automated backup retention: 7 days
- Manual snapshot: `cpsc4910-team01-snapshot`

This document provides the current disaster recovery procedure for the Good (Truck) Driver Incentive Program and should be updated as the project architecture and deployment process evolve.

This document was drafted and formatted with the assistance of AI (chatGPT) and reviewed for accuracy by the author 