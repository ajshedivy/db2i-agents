# 🛠️ IBM i Services Examples

This directory contains examples that demonstrate how to use AI agents to interact with various IBM i Services. These examples showcase SQL interfaces to system information including PTF management, Integrated File System operations, Java Virtual Machine monitoring, and SQL services exploration.

## 🚨 Before You Start

**Have you completed the main setup?** These examples require the environment setup from the main README.

✅ **Required**: Complete the [Getting Started guide](../../../README.md#-getting-started) first, which covers:
- Setting up Mapepire on IBM i
- Creating your `.env` file with database credentials  
- Installing uv package manager
- Choosing your AI model provider

If you haven't done this yet, **stop here** and complete the main setup first.

## 📋 Available Examples

| Category | Example | Description | Difficulty |
|----------|---------|-------------|------------|
| **PTF Services** | 🔍 [Basic PTF Info](ptf/get_ptf_info.py) | Retrieve basic PTF information using AI | Beginner ⭐ |
| | 🔬 [Enhanced PTF Analysis](ptf/get_ptf_info_extended.py) | Detailed PTF information with enhanced AI analysis | Intermediate ⭐⭐ |
| | ⛳ [PTF Golf](ptf/get_ptf_info_golf.py) | Compact PTF information retrieval | Beginner ⭐ |
| **IFS Services** | 📂 [Stream File Reader](ifs/read_stream_file.py) | Read and search file contents in the Integrated File System | Intermediate ⭐⭐ |
| | 💾 [Storage Assistant](ifs/storage_assistant.py) | Find and analyze large files in the Integrated File System | Intermediate ⭐⭐ |
| **Java Services** | ☕ [JVM Assistant](java/jvm_assistant.py) | Monitor and optimize Java Virtual Machines on IBM i | Advanced ⭐⭐⭐ |
| **SQL Services** | 🗃️ [SQL Services Agent](sql_services_agent.py) | Interactive CLI for exploring IBM i SQL services | Intermediate ⭐⭐ |
| | 📓 [SQL Services Info Notebook](sql_services_info.ipynb) | Jupyter notebook demonstrating SQL services queries | Beginner ⭐ |

## 🚀 Running the Examples

Since you've completed the main setup, you can run these service examples directly:

### Running Examples by Category

#### PTF (Program Temporary Fix) Services

```bash
# Basic PTF information
uv run ptf/get_ptf_info.py

# Enhanced PTF analysis with AI
uv run ptf/get_ptf_info_extended.py

# Compact PTF implementation
uv run ptf/get_ptf_info_golf.py
```

#### IFS (Integrated File System) Services

```bash
# Read and search files in IFS
uv run ifs/read_stream_file.py

# Analyze storage usage and large files
uv run ifs/storage_assistant.py
```

#### Java Services

```bash
# Monitor JVM performance
uv run java/jvm_assistant.py
```

#### SQL Services

```bash
# Interactive SQL services exploration
uv run sql_services_agent.py

# Open Jupyter notebook
jupyter notebook sql_services_info.ipynb
```

## 🔍 Example Details

### 🔧 PTF Services Examples

#### 🔍 Basic PTF Info
- Retrieve PTF information using SQL services
- Basic AI analysis of PTF status and recommendations
- Simple command-line interface

#### 🔬 Enhanced PTF Analysis
- Comprehensive PTF analysis with detailed reporting
- AI-powered recommendations for PTF application
- Advanced filtering and search capabilities

#### ⛳ PTF Golf
- Minimal implementation for quick PTF checks
- Compact code demonstrating essential concepts
- Fast PTF status retrieval

### 📁 IFS Services Examples

#### 📂 Stream File Reader
- Read file contents from the Integrated File System
- Search and analyze text files with AI assistance
- Handle various file encodings and formats

#### 💾 Storage Assistant
- Analyze IFS storage usage and patterns
- Identify large files and space consumption
- AI-powered storage optimization recommendations

### ☕ Java Services Examples

#### ☕ JVM Assistant
- Monitor Java Virtual Machine performance on IBM i
- Analyze heap usage, garbage collection, and threading
- AI-powered JVM tuning recommendations
- Integration with IBM i Java management services

### 🗃️ SQL Services Examples

#### 🗃️ SQL Services Agent
- Interactive exploration of IBM i SQL services
- Dynamic query generation and execution
- AI-powered result interpretation and insights

#### 📓 SQL Services Info Notebook
- Jupyter notebook for educational exploration
- Step-by-step SQL services demonstrations
- Interactive examples and visualizations

## 📚 IBM i Services Resources

These examples use various IBM i SQL services:

### PTF Services
**QSYS2 Services:**
- `QSYS2.PTF_INFO` - General PTF information
- `QSYS2.GROUP_PTF_INFO` - PTF group information

**SYSTOOLS Services:**
- `SYSTOOLS.GROUP_PTF_CURRENCY` - PTF group currency status
- `SYSTOOLS.GROUP_PTF_DETAILS` - PTF group details and missing PTFs
- `SYSTOOLS.FIRMWARE_CURRENCY` - Firmware currency information

### IFS Services
**QSYS2 Services:**
- `QSYS2.IFS_READ` - Read file contents from IFS
- `QSYS2.IFS_OBJECT_STATISTICS` - IFS object statistics and file information
- `QSYS2.OBJECT_OWNERSHIP` - Objects owned by users

### Java Services
**QSYS2 Services:**
- `QSYS2.JVM_INFO` - Java Virtual Machine information including garbage collection, heap usage, and performance metrics

### General SQL Services
**QSYS2 Services:**
- `QSYS2.SERVICES_INFO` - Comprehensive information about all available IBM i SQL services

## 🛠️ Customizing Examples

Each example can be customized by:

1. **Database Connection**: Modify connection details in the `.env` file
2. **Service Parameters**: Adjust SQL service parameters and filters
3. **AI Model Configuration**: Change model settings for different analysis styles
4. **Output Formats**: Customize result presentation and reporting
5. **Integration**: Connect with external monitoring tools
6. **Automation**: Add scheduling and automated execution

### Example Customizations:

```python
# PTF filtering
PTF_FILTERS = {
    "product_id": "5770SS1",
    "status": "APPLIED",
    "creation_date": "2024-01-01"
}

# IFS search patterns
IFS_SEARCH_PATTERNS = [
    "/QSYS.LIB/*.LIB/*.FILE",
    "/tmp/large_files/*",
    "/home/*/logs/*.log"
]

# JVM monitoring thresholds
JVM_THRESHOLDS = {
    "heap_usage_percent": 80,
    "gc_frequency": 100,
    "thread_count": 500
}
```

## 🎯 Service Integration Patterns

Common patterns for IBM i service integration:

### Real-time Monitoring
```python
# Continuous monitoring with alerts
def monitor_service(service_function, threshold, interval=60):
    while True:
        result = service_function()
        if check_threshold(result, threshold):
            send_alert(result)
        time.sleep(interval)
```

### Batch Analysis
```python
# Periodic batch analysis
def batch_analysis(services, schedule="daily"):
    for service in services:
        data = collect_service_data(service)
        analysis = ai_analyze(data)
        store_results(analysis)
```

### Predictive Analytics
```python
# AI-powered trend analysis
def predict_trends(historical_data, forecast_days=30):
    model = train_model(historical_data)
    predictions = model.predict(forecast_days)
    return generate_recommendations(predictions)
```

## 📈 Learning Progression

For effective learning, follow this progression:

1. **Start with SQL Services**: Understand the foundation
2. **Try PTF Examples**: Learn system management concepts
3. **Explore IFS Services**: Understand file system integration
4. **Advanced Java Monitoring**: Learn performance analysis

## 📌 Next Steps

After exploring these examples, you can:

1. Combine multiple services for comprehensive system monitoring
2. Create automated maintenance workflows
3. Build custom dashboards integrating various services
4. Develop predictive maintenance solutions
5. Explore integration with external monitoring platforms

## 🚨 Important Considerations

### Permissions
- Ensure appropriate authorities for accessing system services
- Some services require special authorities (*AUDIT, *ALLOBJ, etc.)
- Test permissions in development environments first

### Performance
- Monitor query performance on large systems
- Use appropriate filtering to limit result sets
- Consider caching for frequently accessed data

### Security
- Follow security best practices when accessing system information
- Log and audit service access appropriately
- Protect sensitive system information

## 🤝 Contributing

To contribute new service examples:

1. Follow established patterns for each service category
2. Include comprehensive error handling
3. Document required authorities and permissions
4. Provide clear usage examples and best practices
5. Test with various IBM i system configurations
6. Include integration examples with other services

## 🔗 Related Resources

- [IBM i SQL Services Documentation](https://www.ibm.com/docs/en/i/7.5?topic=services-sql)