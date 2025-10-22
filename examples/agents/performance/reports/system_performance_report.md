# IBM i System Performance Report

### 1. System Overview
- **Total Jobs in System**: 2148
- **Active Jobs**: 709
- **Configured CPUs**: 3
- **Average CPU Utilization**: 59.25%
- **Maximum CPU Utilization**: 77.66%
- **Main Storage Size**: 133 GB
- **System ASP Used**: 48.25%

### 2. Current System Activity
- **Remote Connections**: 82
- **Batch Jobs Running**: 214
- **Batch Jobs on Held Job Queue**: 1416
- **Average CPU Rate**: 83.76

### 3. Memory Pools
- **Base Pool**: 121 GB, Current Threads: 2462
- **Interactive Pool**: 650 MB, Current Threads: 5

### 4. Temporary Storage
- **Named Storage Buckets**: Peaked at 42 GB (Database segment cache being the largest)
- **Unnamed Storage Usage**: Peaked at 31.8 GB

### 5. HTTP Server Metrics
- **Admin Customer Module**: 35,352 Connections, 32,779 Requests Rejected
- **ProfoundUI Server Handled**: 51,680 Connections, 55,835 Requests

### 6. System Values
- **Job Message Queue Size**: 64
- **Max Active Levels**: 32,767
- **Job Activity Level**: 200
- **Max Jobs Allowed**: 165,000

### 7. Collection Services Configuration
- **Active Collection Library**: QPFRDATA
- **Default Collection Interval**: 900 seconds
- **Collection Profile**: *STANDARDP
- **Retention Days**: 30

### 8. Top CPU Consuming Jobs
- **Job 1**: QP0ZSPWT by QUSER in QUSRWRK - 255,718,723 CPU Time
- **Job 2**: QP0ZSPWT by QUSER in QUSRWRK - 253,473,408 CPU Time

This report highlights the overall system performance, identifying key areas of utilization and potential bottlenecks, such as high batch job queues and peak memory usage in specific pools. If you have specific questions or need further analysis on any section, feel free to ask!