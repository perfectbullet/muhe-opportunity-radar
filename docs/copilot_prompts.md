# GitHub Copilot 提示词模板库

本文档提供了针对 Muhe Opportunity Radar 项目的 GitHub Copilot 提示词模板，帮助你高效开发 Vue3 + FastAPI 架构。

---

## 📦 后端开发提示词

### 1. 创建新的 API 路由

```
Create a new FastAPI router file at api/routers/portfolio.py that:
1. Defines endpoints for portfolio management (/api/v1/portfolio)
2. Includes POST /add, GET /list, DELETE /{id} endpoints
3. Uses Pydantic models from api/models/
4. Follows the same structure as api/routers/analysis.py
5. Includes proper error handling with HTTPException
6. Adds docstrings and type hints
```

### 2. 扩展 Service 层

```
Add a new method to api/services/analysis_service.py:
- Method name: analyze_with_history
- Parameters: material (str), investor_id (str), use_history (bool)
- Functionality: 
  1. Get recent analysis for similar materials from MongoDB
  2. Include historical context in the prompt
  3. Call LLM with enhanced prompt
  4. Return analysis with confidence score
- Use async/await for database calls
- Add proper error handling and logging
```

### 3. 实现流式响应

```
Convert the synchronous PerspectiveAnalyzer.analyze_from_perspective() method to support streaming:
1. Make it an async generator function
2. Yield text chunks from LLM response
3. Maintain the same interface as much as possible
4. Update api/services/analysis_service.py to use the new streaming method
5. Ensure proper error handling in the stream

Reference the existing analyze_single_stream method in api/routers/analysis.py
```

### 4. 添加数据验证

```
Create Pydantic validators for api/models/requests.py:
1. Validate material length (min 10, max 10000 characters)
2. Validate investor_id against known investors list
3. Sanitize HTML/script tags from input
4. Add custom error messages for validation failures
5. Use Field validators and model validators

Example for AnalysisRequest model
```

### 5. 集成缓存机制

```
Implement Redis caching for analysis results:
1. Create a new file api/services/cache_service.py
2. Use redis-py library
3. Cache key pattern: "analysis:{investor_id}:{hash(material)}"
4. TTL: 24 hours
5. Wrap AnalysisService.analyze_single to check cache first
6. Add cache invalidation method
```

---

## 🎨 前端开发提示词

### 1. 创建新页面组件

```
Create a Vue3 page component at frontend/src/views/Portfolio.vue:
- Use Composition API with <script setup lang="ts">
- Include Naive UI components: n-card, n-data-table, n-button
- Features:
  1. Display user's investment portfolio in a table
  2. Add new investment button with modal form
  3. Delete investment with confirmation dialog
  4. Real-time update using Pinia store
- Integrate with API: getAllPortfolio, addPortfolio, deletePortfolio from @/api
- Add loading states and error handling with n-message
- Style with TailwindCSS and glass-card effect like other views
```

### 2. 开发可复用组件

```
Create a reusable MarkdownRenderer component at frontend/src/components/MarkdownRenderer.vue:
- Props: content (string), maxHeight (number, optional)
- Features:
  1. Render markdown using markdown-it
  2. Syntax highlighting with highlight.js
  3. Scrollable with custom scrollbar
  4. Support dark theme
  5. Copy code button for code blocks
- Use Composition API
- Export as default and register globally in main.ts
```

### 3. 实现流式数据接收

```
Update frontend/src/views/SingleAnalysis.vue to support streaming analysis:
1. Add a "流式分析" toggle button
2. When enabled, use EventSource to connect to /api/v1/analyze/stream
3. Display analysis text incrementally with typewriter effect
4. Show real-time progress indicator
5. Handle connection errors and auto-reconnect
6. Allow users to stop the stream

Reference the streaming API implementation in frontend/src/api/analysis.ts
```

### 4. 添加数据可视化

```
Create an ECharts component for multi-investor comparison visualization:
- Component: frontend/src/components/InvestorRadarChart.vue
- Props: investors (array of {name, scores: {value, risk, longTerm, ...}})
- Chart type: Radar chart
- Features:
  1. Compare up to 5 investors simultaneously
  2. Interactive legend to show/hide investors
  3. Responsive design
  4. Dark theme compatible colors
  5. Tooltip showing detailed scores
- Use vue-echarts wrapper
- Add to MultiComparison.vue page
```

### 5. 状态管理优化

```
Create a Pinia store at frontend/src/stores/analysis.ts:
- State:
  - currentAnalysis (AnalysisResponse | null)
  - analysisHistory (AnalysisResponse[])
  - selectedInvestors (string[])
  - isAnalyzing (boolean)
- Actions:
  - analyzeSingle(material, investorId): Call API and update state
  - compareMultiple(material, investorIds): Multi-perspective analysis
  - loadHistory(): Fetch from localStorage
  - clearHistory()
- Getters:
  - recentAnalyses: Last 5 analyses
  - favoriteInvestors: Most used investors
- Persist state to localStorage
```

### 6. 实现搜索高亮

```
Add search highlighting to frontend/src/views/HistoryRecords.vue:
1. When search results are displayed, highlight matching keywords
2. Use a utility function to wrap keywords in <mark> tags
3. Apply custom styling to <mark> with TailwindCSS
4. Case-insensitive matching
5. Highlight multiple keywords
6. Don't break markdown formatting

Create utility function in frontend/src/utils/highlight.ts
```

---

## 🔄 全栈功能提示词

### 1. 添加导出功能

```
Implement PDF export feature for analysis results:

Backend (FastAPI):
1. Add dependency: reportlab or weasyprint
2. Create new endpoint: POST /api/v1/export/pdf
3. Accept analysis record_id
4. Generate PDF with:
   - Company logo header
   - Analysis metadata (date, investor, material)
   - Formatted analysis content
   - Charts/graphs if present
5. Return PDF as StreamingResponse

Frontend (Vue3):
1. Add "导出 PDF" button to analysis result card
2. Call export API endpoint
3. Download file using browser download API
4. Show loading state during generation
5. Handle errors gracefully
```

### 2. 实现用户认证

```
Add JWT-based authentication system:

Backend:
1. Install python-jose, passlib
2. Create api/auth.py with:
   - login endpoint (POST /api/v1/auth/login)
   - register endpoint (POST /api/v1/auth/register)
   - JWT token generation and validation
   - Password hashing
3. Add authentication dependency to protected routes
4. Store user info in MongoDB users collection

Frontend:
1. Create login/register pages
2. Store JWT token in localStorage
3. Add token to axios request interceptor
4. Implement logout functionality
5. Redirect to login if token expired
6. Create auth store with Pinia

Update Copilot instructions with security best practices
```

### 3. 添加实时通知

```
Implement real-time notifications using WebSocket:

Backend:
1. Add websockets dependency to FastAPI
2. Create WebSocket endpoint at /api/v1/ws
3. Broadcast events:
   - New analysis completed
   - Analysis failed
   - System notifications
4. Maintain connected clients list
5. Handle reconnection

Frontend:
1. Create WebSocket client in frontend/src/api/websocket.ts
2. Connect on app mount
3. Display notifications using n-notification
4. Auto-reconnect on disconnect
5. Show connection status indicator
6. Store notifications in Pinia store
```

---

## 🐳 DevOps 提示词

### 1. 优化 Docker 构建

```
Optimize Dockerfile.api for faster builds and smaller image:
1. Use multi-stage build
2. Install only production dependencies
3. Use .dockerignore to exclude unnecessary files
4. Leverage build cache with proper layer ordering
5. Add health check endpoint
6. Use non-root user for security
7. Set proper environment variables

Also update docker-compose.yml with:
- Resource limits
- Restart policies
- Health checks
- Volume mounts for development
```

### 2. CI/CD 流水线

```
Create GitHub Actions workflow at .github/workflows/deploy.yml:
1. Trigger on push to main branch
2. Jobs:
   - test-backend: Run pytest for Python code
   - test-frontend: Run vitest for Vue3 code
   - build: Build Docker images
   - deploy: Deploy to production server
3. Use secrets for API keys
4. Send notifications on failure
5. Add status badge to README

Include steps for:
- Linting (flake8, eslint)
- Type checking (mypy, vue-tsc)
- Security scanning (safety, npm audit)
```

---

## 📊 数据分析提示词

### 1. 生成分析报告

```
Create an automated analysis report generator:
1. Aggregate statistics from MongoDB:
   - Total analyses per investor
   - Average analysis time
   - Most analyzed companies
   - Success/failure rates
2. Generate insights:
   - Trending investors
   - Popular analysis times
   - Correlation between investor types and results
3. Create visualizations with matplotlib or plotly
4. Export as HTML dashboard
5. Schedule daily generation with APScheduler

Add new endpoint: GET /api/v1/reports/daily
Frontend: Display in new Reports page with date picker
```

### 2. 机器学习集成

```
Add ML-based material quality scoring:
1. Train a simple classifier to predict analysis quality
2. Features:
   - Material length
   - Keyword presence
   - Numerical data ratio
   - Structure (sections, bullet points)
3. Use scikit-learn for training
4. Save model with joblib
5. Add prediction endpoint: POST /api/v1/predict/quality
6. Display quality score before analysis submission
7. Suggest improvements for low-quality materials

Frontend: Show score with n-progress component and tips
```

---

## 🎯 使用技巧

### 1. 组合多个提示词

将简单提示词组合成复杂功能：

```
Context: I'm working on the Muhe Opportunity Radar project with Vue3 + FastAPI architecture.

Task 1: [后端提示词]
Task 2: [前端提示词]
Task 3: [集成测试提示词]

Please implement these in order and ensure they work together seamlessly.
```

### 2. 指定代码风格

```
Follow these code style guidelines:
- Python: PEP 8, type hints, docstrings
- TypeScript: Airbnb style, explicit types
- Vue3: Composition API, <script setup>
- Use async/await consistently
- Add error handling to all external calls
- Include unit tests for new functions
```

### 3. 请求代码审查

```
Review the following code from [file_path]:
1. Check for security vulnerabilities
2. Suggest performance optimizations
3. Identify potential bugs
4. Recommend better patterns or practices
5. Verify error handling is comprehensive

Provide specific suggestions with code examples.
```

### 4. 调试帮助

```
I'm encountering this error in [file]:
[paste error message]

Context:
- What I'm trying to do: [description]
- Steps to reproduce: [steps]
- Expected behavior: [expectation]
- Actual behavior: [reality]

Please help diagnose the issue and provide a fix.
```

---

## 📝 最佳实践

1. **明确上下文**：始终说明你在哪个文件或模块工作
2. **具体需求**：详细描述功能要求，而非模糊概念
3. **参考现有代码**：让 Copilot 参考项目中类似实现
4. **分步骤**：复杂功能拆分为多个小步骤
5. **包含约束**：明确性能、安全、兼容性要求
6. **请求测试**：要求生成对应的单元测试
7. **迭代改进**：根据第一次生成的代码继续优化

---

## 🔗 相关资源

- [GitHub Copilot 文档](https://docs.github.com/copilot)
- [FastAPI 最佳实践](https://fastapi.tiangolo.com/async/)
- [Vue3 风格指南](https://vuejs.org/style-guide/)
- [Naive UI 组件示例](https://www.naiveui.com/zh-CN/os-theme/components/button)

**Happy Coding with Copilot! 🚀**
