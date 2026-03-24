import { type TestCase, type Execution, type DashboardStats, type ActivityItem, type ZephyrConfig, type User, type ExecutionSummary } from '@/types'

const delay = (ms: number) => new Promise(res => setTimeout(res, ms))

// ─── Mock Users ───────────────────────────────────────────────────────────────
export const mockUser: User = {
  id: 'u1',
  name: 'Alex Johnson',
  email: 'alex@testai.io',
  role: 'admin',
}

// ─── Mock Test Cases ──────────────────────────────────────────────────────────
export const mockTestCases: TestCase[] = [
  {
    id: 'TC-001',
    title: 'User Login with Valid Credentials',
    description: 'Verify that users can log in with valid username and password',
    type: 'UI',
    status: 'approved',
    bddContent: `Feature: User Authentication
  As a registered user
  I want to log in to the application
  So that I can access my account

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter valid username "user@example.com"
    And I enter valid password "SecurePass123"
    And I click the Login button
    Then I should be redirected to the dashboard
    And I should see a welcome message "Welcome, Alex"

  Scenario: Failed login with invalid password
    Given I am on the login page
    When I enter username "user@example.com"
    And I enter invalid password "wrongpass"
    And I click the Login button
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page`,
    seleniumCode: `import org.openqa.selenium.WebDriver;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.testng.annotations.Test;
import org.testng.Assert;

public class UserLoginTest extends BaseTest {

    @Test(description = "Verify successful login with valid credentials")
    public void testSuccessfulLogin() {
        driver.get(BASE_URL + "/login");
        
        WebElement emailField = driver.findElement(By.id("email"));
        WebElement passwordField = driver.findElement(By.id("password"));
        WebElement loginBtn = driver.findElement(By.id("login-btn"));
        
        emailField.sendKeys("user@example.com");
        passwordField.sendKeys("SecurePass123");
        loginBtn.click();
        
        WebElement welcomeMsg = wait.until(
            ExpectedConditions.visibilityOfElementLocated(By.className("welcome-msg"))
        );
        
        Assert.assertTrue(welcomeMsg.isDisplayed(), "Welcome message should be visible");
        Assert.assertEquals(driver.getCurrentUrl(), BASE_URL + "/dashboard");
    }

    @Test(description = "Verify failed login with invalid password")
    public void testInvalidCredentials() {
        driver.get(BASE_URL + "/login");
        
        driver.findElement(By.id("email")).sendKeys("user@example.com");
        driver.findElement(By.id("password")).sendKeys("wrongpass");
        driver.findElement(By.id("login-btn")).click();
        
        WebElement errorMsg = wait.until(
            ExpectedConditions.visibilityOfElementLocated(By.className("error-msg"))
        );
        
        Assert.assertEquals(errorMsg.getText(), "Invalid credentials");
    }
}`,
    tags: ['authentication', 'login', 'smoke'],
    createdAt: '2026-03-20T10:00:00Z',
    updatedAt: '2026-03-22T14:30:00Z',
    zephyrId: 'ZTC-2341',
    syncStatus: 'synced',
  },
  {
    id: 'TC-002',
    title: 'Product Search - Filter by Category',
    description: 'Validate product search with category filters returns correct results',
    type: 'UI',
    status: 'approved',
    bddContent: `Feature: Product Search
  As a customer
  I want to search and filter products
  So that I can quickly find what I need

  Scenario: Filter products by category
    Given I am on the products page
    When I select category "Electronics"
    And I click "Apply Filter"
    Then I should see only products from "Electronics" category
    And the product count should be updated`,
    seleniumCode: `@Test(description = "Verify product category filter")
public void testCategoryFilter() {
    driver.get(BASE_URL + "/products");
    Select categoryDropdown = new Select(driver.findElement(By.id("category-filter")));
    categoryDropdown.selectByVisibleText("Electronics");
    driver.findElement(By.id("apply-filter")).click();
    
    List<WebElement> products = driver.findElements(By.className("product-card"));
    for (WebElement product : products) {
        String category = product.findElement(By.className("product-category")).getText();
        Assert.assertEquals(category, "Electronics");
    }
}`,
    tags: ['search', 'filter', 'regression'],
    createdAt: '2026-03-21T09:15:00Z',
    updatedAt: '2026-03-22T11:00:00Z',
    zephyrId: 'ZTC-2342',
    syncStatus: 'synced',
  },
  {
    id: 'TC-003',
    title: 'Checkout Flow - Payment Processing',
    description: 'End to end checkout with payment validation',
    type: 'UI',
    status: 'pending',
    bddContent: `Feature: Checkout Payment
  Scenario: Successful payment with valid card
    Given I have items in my cart
    And I am on the checkout page
    When I enter valid card details
    And I click "Place Order"
    Then the order should be confirmed
    And I should receive a confirmation email`,
    seleniumCode: `@Test
public void testPaymentProcessing() {
    // Navigate to checkout
    driver.get(BASE_URL + "/checkout");
    // Fill payment details
    driver.findElement(By.id("card-number")).sendKeys("4111111111111111");
    driver.findElement(By.id("expiry")).sendKeys("12/27");
    driver.findElement(By.id("cvv")).sendKeys("123");
    driver.findElement(By.id("place-order")).click();
    // Verify confirmation
    Assert.assertTrue(driver.findElement(By.id("order-confirmation")).isDisplayed());
}`,
    tags: ['checkout', 'payment', 'e2e'],
    createdAt: '2026-03-23T14:00:00Z',
    updatedAt: '2026-03-23T14:00:00Z',
    syncStatus: 'not_synced',
  },
  {
    id: 'TC-004',
    title: 'API - User Registration Endpoint',
    description: 'Validate POST /api/v1/users returns 201 with correct payload',
    type: 'API',
    status: 'approved',
    bddContent: `Feature: User Registration API
  Scenario: Register new user with valid data
    Given the API endpoint "/api/v1/users" is available
    When I send a POST request with valid user data
    Then the response status should be 201
    And the response body should contain the user ID
    And the Content-Type should be "application/json"`,
    seleniumCode: `@Test
public void testUserRegistrationAPI() throws Exception {
    RestAssured.baseURI = API_BASE_URL;
    
    JSONObject requestBody = new JSONObject();
    requestBody.put("email", "newuser@test.com");
    requestBody.put("password", "SecurePass@123");
    requestBody.put("name", "Test User");
    
    Response response = given()
        .contentType("application/json")
        .body(requestBody.toString())
        .when()
        .post("/api/v1/users")
        .then()
        .statusCode(201)
        .extract().response();
    
    Assert.assertNotNull(response.jsonPath().get("id"));
}`,
    tags: ['api', 'registration', 'smoke'],
    createdAt: '2026-03-22T16:00:00Z',
    updatedAt: '2026-03-23T09:00:00Z',
    zephyrId: 'ZTC-2343',
    syncStatus: 'synced',
  },
  {
    id: 'TC-005',
    title: 'Password Reset Email Flow',
    description: 'Verify password reset email is sent and link works',
    type: 'UI',
    status: 'rejected',
    bddContent: `Feature: Password Reset
  Scenario: Request password reset
    Given I am on the forgot password page
    When I enter my registered email
    And I click "Send Reset Link"
    Then I should see success message
    And a reset email should be sent`,
    seleniumCode: `@Test
public void testPasswordReset() {
    driver.get(BASE_URL + "/forgot-password");
    driver.findElement(By.id("email")).sendKeys("user@example.com");
    driver.findElement(By.id("send-reset")).click();
    Assert.assertTrue(driver.findElement(By.className("success-banner")).isDisplayed());
}`,
    tags: ['auth', 'password-reset'],
    createdAt: '2026-03-20T11:30:00Z',
    updatedAt: '2026-03-21T08:45:00Z',
    syncStatus: 'failed',
  },
  {
    id: 'TC-006',
    title: 'Dashboard KPI Cards Load',
    description: 'Regression test for dashboard analytics widgets',
    type: 'Regression',
    status: 'pending',
    bddContent: `Feature: Dashboard Analytics
  Scenario: KPI cards display correct data
    Given I am logged in as admin
    And I am on the dashboard page
    Then I should see the "Total Sales" KPI card
    And I should see the "Active Users" KPI card
    And all values should be numeric`,
    seleniumCode: `@Test
public void testDashboardKPIs() {
    loginAs("admin");
    driver.get(BASE_URL + "/dashboard");
    WebElement totalSales = driver.findElement(By.id("kpi-total-sales"));
    Assert.assertTrue(totalSales.isDisplayed());
    Assert.assertTrue(totalSales.getText().matches("\\$[\\d,]+"));
}`,
    tags: ['dashboard', 'regression', 'analytics'],
    createdAt: '2026-03-24T08:00:00Z',
    updatedAt: '2026-03-24T08:00:00Z',
    syncStatus: 'not_synced',
  },
]

// ─── Mock Executions ──────────────────────────────────────────────────────────
export const mockExecution: Execution = {
  id: 'EX-20260324-001',
  testCaseIds: ['TC-001', 'TC-002', 'TC-004'],
  status: 'passed',
  startTime: '2026-03-24T12:00:00Z',
  endTime: '2026-03-24T12:08:32Z',
  pipeline: 'harness-pipeline-main',
  logs: [
    { timestamp: '12:00:01', level: 'action', message: 'Initializing Harness pipeline...' },
    { timestamp: '12:00:03', level: 'info', message: 'Pulling latest test artifacts from artifact store' },
    { timestamp: '12:00:08', level: 'info', message: 'Setting up WebDriver environment (Chrome 122)' },
    { timestamp: '12:00:15', level: 'action', message: '[TC-001] Starting: User Login with Valid Credentials' },
    { timestamp: '12:01:02', level: 'success', message: '[TC-001] PASSED in 47.3s' },
    { timestamp: '12:01:05', level: 'action', message: '[TC-002] Starting: Product Search - Filter by Category' },
    { timestamp: '12:02:10', level: 'success', message: '[TC-002] PASSED in 65.2s' },
    { timestamp: '12:02:13', level: 'action', message: '[TC-004] Starting: API - User Registration Endpoint' },
    { timestamp: '12:02:45', level: 'success', message: '[TC-004] PASSED in 32.1s' },
    { timestamp: '12:02:46', level: 'success', message: 'All 3 tests passed. Pipeline execution complete.' },
  ],
}

// ─── Mock Results ─────────────────────────────────────────────────────────────
export const mockExecutionSummary: ExecutionSummary = {
  executionId: 'EX-20260324-001',
  totalTests: 3,
  passed: 3,
  failed: 0,
  skipped: 0,
  duration: 512,
  passRate: 100,
  results: [
    {
      testCaseId: 'TC-001',
      testCaseTitle: 'User Login with Valid Credentials',
      status: 'passed',
      duration: 47300,
      logs: [
        { timestamp: '12:00:15', level: 'action', message: 'Navigating to /login' },
        { timestamp: '12:00:18', level: 'info', message: 'Entering credentials' },
        { timestamp: '12:01:02', level: 'success', message: 'Login successful, dashboard loaded' },
      ],
      screenshots: ['screenshot_TC001_pass.png'],
      artifacts: ['report_TC001.html'],
      aiInsight: undefined,
    },
    {
      testCaseId: 'TC-002',
      testCaseTitle: 'Product Search - Filter by Category',
      status: 'passed',
      duration: 65200,
      logs: [
        { timestamp: '12:01:05', level: 'action', message: 'Loading products page' },
        { timestamp: '12:01:12', level: 'info', message: 'Selecting Electronics category' },
        { timestamp: '12:02:10', level: 'success', message: '24 products matched filter' },
      ],
      screenshots: ['screenshot_TC002_pass.png'],
      artifacts: ['report_TC002.html'],
    },
    {
      testCaseId: 'TC-004',
      testCaseTitle: 'API - User Registration Endpoint',
      status: 'passed',
      duration: 32100,
      logs: [
        { timestamp: '12:02:13', level: 'action', message: 'POST /api/v1/users' },
        { timestamp: '12:02:44', level: 'success', message: '201 Created - user ID: usr_abc123' },
      ],
      screenshots: [],
      artifacts: ['api_report_TC004.json'],
    },
  ],
}

// ─── Mock Dashboard Stats ─────────────────────────────────────────────────────
export const mockDashboardStats: DashboardStats = {
  totalTestCases: 6,
  passed: 3,
  failed: 1,
  recentExecutions: 4,
}

export const mockActivityFeed: ActivityItem[] = [
  { id: 'a1', type: 'executed', title: 'Execution EX-20260324-001 completed (3 passed)', timestamp: '2026-03-24T12:08:00Z', user: 'Alex Johnson' },
  { id: 'a2', type: 'synced', title: 'TC-004 synced to Zephyr (ZTC-2343)', timestamp: '2026-03-23T09:05:00Z', user: 'Alex Johnson' },
  { id: 'a3', type: 'approved', title: 'TC-002 approved and pushed to Zephyr', timestamp: '2026-03-22T11:00:00Z', user: 'Alex Johnson' },
  { id: 'a4', type: 'generated', title: '6 test cases generated from Confluence page', timestamp: '2026-03-20T10:30:00Z', user: 'Alex Johnson' },
  { id: 'a5', type: 'failed', title: 'TC-005 rejected - missing assertions', timestamp: '2026-03-21T08:45:00Z', user: 'Alex Johnson' },
]

// ─── Mock Zephyr Config ───────────────────────────────────────────────────────
export const mockZephyrConfig: ZephyrConfig = {
  connected: true,
  projectKey: 'ESHOP',
  baseUrl: 'https://zephyr.atlassian.net',
  lastSync: '2026-03-24T12:00:00Z',
}

// ─── API Functions (simulated) ────────────────────────────────────────────────

export const api = {
  async getDashboardStats() {
    await delay(800)
    return mockDashboardStats
  },

  async getActivityFeed() {
    await delay(600)
    return mockActivityFeed
  },

  async getTestCases() {
    await delay(900)
    return [...mockTestCases]
  },

  async getTestCase(id: string) {
    await delay(400)
    const tc = mockTestCases.find(t => t.id === id)
    if (!tc) throw new Error(`Test case ${id} not found`)
    return { ...tc }
  },

  async updateTestCase(id: string, patch: Partial<TestCase>) {
    await delay(500)
    const idx = mockTestCases.findIndex(t => t.id === id)
    if (idx === -1) throw new Error(`Test case ${id} not found`)
    Object.assign(mockTestCases[idx], patch, { updatedAt: new Date().toISOString() })
    return { ...mockTestCases[idx] }
  },

  async deleteTestCase(id: string) {
    await delay(400)
    const idx = mockTestCases.findIndex(t => t.id === id)
    if (idx !== -1) mockTestCases.splice(idx, 1)
  },

  async generateTestCases(_input: unknown, onLog: (msg: string) => void) {
    const steps = [
      { msg: 'Parsing prompt and extracting key requirements...', delay: 1200 },
      { msg: 'Fetching Confluence page: ESHOP-Architecture...', delay: 1500 },
      { msg: 'Fetching Jira ticket: ESHOP-4521 - Checkout Flow...', delay: 1000 },
      { msg: 'Sending context to AI model (gemini-2.0-flash)...', delay: 2000 },
      { msg: 'AI generating BDD scenarios...', delay: 2500 },
      { msg: 'Generating Selenium automation code...', delay: 2000 },
      { msg: 'Post-processing and validating test cases...', delay: 800 },
      { msg: '✓ 3 test cases generated successfully!', delay: 400 },
    ]
    for (const step of steps) {
      await delay(step.delay)
      onLog(step.msg)
    }
    return mockTestCases.slice(0, 3)
  },

  async pushToZephyr(ids: string[], onProgress: (id: string) => void) {
    for (const id of ids) {
      await delay(800)
      onProgress(id)
    }
    return { pushed: ids.length, failed: 0 }
  },

  async runExecution(ids: string[], onLog: (entry: string) => void) {
    const logs = [
      'Initializing Harness pipeline execution...',
      'Pulling test artifacts from registry...',
      'Spinning up Chrome WebDriver nodes...',
      `Running ${ids.length} selected test case(s)...`,
      `[${ids[0]}] STARTED`,
      `[${ids[0]}] Navigating to application URL`,
      `[${ids[0]}] Executing test steps...`,
      `[${ids[0]}] PASSED ✓`,
      ids.length > 1 ? `[${ids[1]}] STARTED` : null,
      ids.length > 1 ? `[${ids[1]}] PASSED ✓` : null,
      'Collecting artifacts and screenshots...',
      'Pipeline execution completed successfully.',
    ].filter(Boolean)

    for (const log of logs) {
      await delay(900)
      onLog(log as string)
    }
    return mockExecution
  },

  async getExecutionResults(_id: string) {
    await delay(700)
    return mockExecutionSummary
  },

  async getZephyrConfig() {
    await delay(500)
    return mockZephyrConfig
  },

  async getSyncedTestCases() {
    await delay(700)
    return mockTestCases.filter(t => t.syncStatus === 'synced')
  },
}
