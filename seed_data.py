"""
Seed script — Real-world courses with Unsplash images.
Run: python manage.py shell < seed_data.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ednova.settings')
django.setup()

from core.models import Course, Lesson, Quiz

# ═══════════════════════════════════════════════════
# COURSE 1: Machine Learning Fundamentals
# ═══════════════════════════════════════════════════
c1 = Course.objects.create(
    title="Machine Learning Fundamentals",
    description="A comprehensive introduction to machine learning — from linear regression to neural networks. Build real predictive models using Python and scikit-learn.",
    thumbnail_url="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80",
    icon_emoji="🧠"
)

l1 = Lesson.objects.create(
    course=c1, title="What is Machine Learning?", order=1,
    thumbnail_url="https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=600&q=80",
    content="""# What is Machine Learning?

Machine Learning (ML) is a subset of Artificial Intelligence that enables computers to **learn from data** without being explicitly programmed. Instead of writing rules by hand, we feed data into algorithms that automatically find patterns.

## The Three Types of Machine Learning

### 1. Supervised Learning
The algorithm learns from **labeled data** — input-output pairs where the correct answer is known.

- **Classification**: Predicting categories (spam vs. not spam, cat vs. dog)
- **Regression**: Predicting continuous values (house prices, stock prices)

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)  # Learn from labeled data
predictions = model.predict(X_test)  # Predict new values
```

### 2. Unsupervised Learning
The algorithm discovers **hidden patterns** in unlabeled data.

- **Clustering**: Grouping similar items (customer segmentation)
- **Dimensionality Reduction**: Compressing data while preserving structure (PCA)

### 3. Reinforcement Learning
The agent learns by **trial and error**, receiving rewards for good actions.

- Used in robotics, game playing (AlphaGo), autonomous vehicles

## Real-World Applications

| Industry | Application | ML Type |
|----------|-------------|---------|
| Healthcare | Disease diagnosis from X-rays | Supervised (Classification) |
| Finance | Fraud detection | Supervised (Classification) |
| Retail | Customer segmentation | Unsupervised (Clustering) |
| Self-driving | Navigation decisions | Reinforcement Learning |

## The ML Workflow

1. **Collect Data** — Gather relevant, quality datasets
2. **Explore & Clean** — Handle missing values, outliers
3. **Feature Engineering** — Select and transform input variables
4. **Train Model** — Fit algorithm on training data
5. **Evaluate** — Measure performance on test data
6. **Deploy** — Put the model into production

Machine learning is not magic — it's applied statistics at scale, powered by computation."""
)

Quiz.objects.create(
    lesson=l1,
    question="Which type of machine learning uses labeled input-output pairs for training?",
    option_a="Unsupervised Learning",
    option_b="Supervised Learning",
    option_c="Reinforcement Learning",
    option_d="Transfer Learning",
    correct_option="B"
)

l2 = Lesson.objects.create(
    course=c1, title="Linear Regression Deep Dive", order=2,
    thumbnail_url="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=80",
    content="""# Linear Regression Deep Dive

Linear Regression is the foundational algorithm in machine learning. It models the relationship between a dependent variable (y) and one or more independent variables (X) by fitting a straight line.

## The Math Behind It

The equation of a simple linear regression:

**ŷ = w₀ + w₁x**

Where:
- **ŷ** = predicted value
- **w₀** = bias (y-intercept)
- **w₁** = weight (slope)
- **x** = input feature

## Cost Function: Mean Squared Error

We minimize the error between predictions and actual values:

**MSE = (1/n) × Σ(yᵢ - ŷᵢ)²**

The goal is to find w₀ and w₁ that minimize this cost.

## Implementation from Scratch

```python
import numpy as np

class SimpleLinearRegression:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.lr = learning_rate
        self.epochs = epochs
        self.w = 0
        self.b = 0
    
    def fit(self, X, y):
        n = len(X)
        for _ in range(self.epochs):
            y_pred = self.w * X + self.b
            # Gradients
            dw = -(2/n) * np.sum(X * (y - y_pred))
            db = -(2/n) * np.sum(y - y_pred)
            # Update weights
            self.w -= self.lr * dw
            self.b -= self.lr * db
    
    def predict(self, X):
        return self.w * X + self.b
```

## Using scikit-learn

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
print(f"R² Score: {r2_score(y_test, predictions):.4f}")
print(f"MSE: {mean_squared_error(y_test, predictions):.4f}")
```

## Key Assumptions

1. **Linearity** — Relationship between X and y is linear
2. **Independence** — Observations are independent
3. **Homoscedasticity** — Constant variance of residuals
4. **Normality** — Residuals are normally distributed

When these assumptions are violated, consider polynomial regression, decision trees, or other non-linear models."""
)

Quiz.objects.create(
    lesson=l2,
    question="What cost function does Linear Regression typically minimize?",
    option_a="Cross-Entropy Loss",
    option_b="Hinge Loss",
    option_c="Mean Squared Error (MSE)",
    option_d="Log Loss",
    correct_option="C"
)

l3 = Lesson.objects.create(
    course=c1, title="Classification with Decision Trees", order=3,
    thumbnail_url="https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600&q=80",
    content="""# Classification with Decision Trees

Decision Trees are intuitive, powerful models that make predictions by learning a series of if-then-else rules from data. They work for both classification and regression tasks.

## How Decision Trees Work

A decision tree splits data into subsets by asking questions about features:

```
Is income > $50K?
├── Yes → Is age > 30?
│   ├── Yes → Approve Loan ✅
│   └── No  → Review Manually 🔍
└── No  → Is credit score > 700?
    ├── Yes → Approve Loan ✅
    └── No  → Deny Loan ❌
```

## Splitting Criteria

### Gini Impurity (used by CART)
Measures how often a randomly chosen element would be misclassified.

**Gini = 1 - Σ(pᵢ)²**

A Gini of 0 means all elements belong to one class (pure node).

### Information Gain (used by ID3, C4.5)
Based on the concept of entropy from information theory.

**Entropy = -Σ pᵢ × log₂(pᵢ)**

Choose the split that maximizes information gain (reduces entropy the most).

## Implementation with scikit-learn

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Load famous Iris dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42
)

# Train
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
accuracy = clf.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2%}")  # ~97%
```

## Preventing Overfitting

Decision trees are prone to overfitting. Control complexity with:

- **max_depth** — Maximum tree depth
- **min_samples_split** — Minimum samples to split a node
- **min_samples_leaf** — Minimum samples in a leaf node
- **Pruning** — Remove branches that don't improve performance

## From Trees to Forests

**Random Forest** builds many trees on random subsets of data and averages their predictions — dramatically improving accuracy and reducing overfitting.

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
print(f"Random Forest Accuracy: {rf.score(X_test, y_test):.2%}")
```"""
)

Quiz.objects.create(
    lesson=l3,
    question="What does a Gini impurity of 0 indicate about a decision tree node?",
    option_a="The node contains an equal mix of all classes",
    option_b="All elements belong to a single class (pure node)",
    option_c="The node needs further splitting",
    option_d="The tree has overfitted the data",
    correct_option="B"
)

# ═══════════════════════════════════════════════════
# COURSE 2: Full-Stack Web Development
# ═══════════════════════════════════════════════════
c2 = Course.objects.create(
    title="Full-Stack Web Development",
    description="Build modern web applications from front to back. Master React, Node.js, REST APIs, databases, and deployment strategies used by top tech companies.",
    thumbnail_url="https://images.unsplash.com/photo-1547658719-da2b51169166?w=800&q=80",
    icon_emoji="🌐"
)

l4 = Lesson.objects.create(
    course=c2, title="Modern JavaScript ES6+", order=1,
    thumbnail_url="https://images.unsplash.com/photo-1579468118864-1b9ea3c0db4a?w=600&q=80",
    content="""# Modern JavaScript ES6+

ECMAScript 2015 (ES6) and beyond transformed JavaScript from a simple scripting language into a powerful, modern programming language. Let's explore the features every developer must know.

## Arrow Functions

A shorter syntax for function expressions:

```javascript
// Traditional
function add(a, b) { return a + b; }

// Arrow function
const add = (a, b) => a + b;

// With array methods
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
```

## Destructuring

Extract values from arrays and objects elegantly:

```javascript
// Object destructuring
const user = { name: 'Alice', age: 25, role: 'Engineer' };
const { name, age } = user;

// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
// first = 1, second = 2, rest = [3, 4, 5]

// Function parameters
function greet({ name, age }) {
    return `Hi ${name}, you're ${age}!`;
}
```

## Template Literals

String interpolation with backticks:

```javascript
const name = 'World';
const greeting = `Hello, ${name}!`;
const multiLine = `
    This spans
    multiple lines
    naturally.
`;
```

## Promises & Async/Await

Handle asynchronous operations cleanly:

```javascript
// Promise-based
fetch('/api/users')
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => console.error(err));

// Async/Await — cleaner syntax
async function getUsers() {
    try {
        const res = await fetch('/api/users');
        const data = await res.json();
        return data;
    } catch (err) {
        console.error('Failed:', err);
    }
}
```

## Spread & Rest Operators

```javascript
// Spread — expand arrays/objects
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5]; // [1, 2, 3, 4, 5]

const defaults = { theme: 'dark', lang: 'en' };
const settings = { ...defaults, lang: 'fr' }; // Override lang

// Rest — collect remaining items
function sum(...numbers) {
    return numbers.reduce((a, b) => a + b, 0);
}
```

## Modules (import/export)

```javascript
// math.js
export const PI = 3.14159;
export function circumference(r) { return 2 * PI * r; }

// app.js
import { PI, circumference } from './math.js';
```

Master these features and you'll write cleaner, more expressive JavaScript."""
)

Quiz.objects.create(
    lesson=l4,
    question="What does the spread operator (...) do when used with an array?",
    option_a="Deletes all elements from the array",
    option_b="Expands the array into individual elements",
    option_c="Sorts the array in ascending order",
    option_d="Creates a deep copy of nested objects",
    correct_option="B"
)

l5 = Lesson.objects.create(
    course=c2, title="RESTful API Design", order=2,
    thumbnail_url="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=80",
    content="""# RESTful API Design

REST (Representational State Transfer) is the dominant architectural style for web APIs. Understanding REST principles is essential for any full-stack developer.

## REST Principles

1. **Client-Server** — Separation of concerns
2. **Stateless** — Each request contains all needed information
3. **Cacheable** — Responses can be cached for performance
4. **Uniform Interface** — Consistent URL patterns and HTTP methods
5. **Layered System** — Client doesn't know if it's talking to the end server

## HTTP Methods & CRUD

| Method | CRUD | Example | Description |
|--------|------|---------|-------------|
| GET | Read | `GET /api/users` | List all users |
| GET | Read | `GET /api/users/42` | Get user #42 |
| POST | Create | `POST /api/users` | Create new user |
| PUT | Update | `PUT /api/users/42` | Replace user #42 |
| PATCH | Partial Update | `PATCH /api/users/42` | Update fields of user #42 |
| DELETE | Delete | `DELETE /api/users/42` | Delete user #42 |

## URL Design Best Practices

```
✅ Good:
GET    /api/v1/courses
GET    /api/v1/courses/5
GET    /api/v1/courses/5/lessons
POST   /api/v1/courses/5/lessons
GET    /api/v1/courses?category=science&page=2

❌ Bad:
GET    /api/getCourses
POST   /api/createNewLesson
GET    /api/course_list
```

**Rules:**
- Use **nouns**, not verbs
- Use **plural** resource names
- Use **kebab-case** for multi-word names
- Nest related resources logically

## Status Codes

```
2xx — Success
  200 OK — Request succeeded
  201 Created — Resource created
  204 No Content — Deleted successfully

4xx — Client Error
  400 Bad Request — Invalid input
  401 Unauthorized — Authentication required
  403 Forbidden — Insufficient permissions
  404 Not Found — Resource doesn't exist
  422 Unprocessable Entity — Validation failed

5xx — Server Error
  500 Internal Server Error — Something broke
  503 Service Unavailable — Temporarily down
```

## Authentication Strategies

- **API Keys** — Simple, but limited security
- **JWT (JSON Web Tokens)** — Stateless, scalable
- **OAuth 2.0** — Third-party authorization (Google, GitHub login)
- **Session Cookies** — Traditional, stateful

## Pagination, Filtering & Sorting

```json
GET /api/courses?page=2&limit=20&sort=-created_at&category=ml

Response:
{
    "data": [...],
    "meta": {
        "total": 156,
        "page": 2,
        "per_page": 20,
        "total_pages": 8
    }
}
```

Well-designed APIs are a joy to consume and maintain."""
)

Quiz.objects.create(
    lesson=l5,
    question="Which HTTP status code should be returned when a new resource is successfully created?",
    option_a="200 OK",
    option_b="201 Created",
    option_c="204 No Content",
    option_d="301 Moved Permanently",
    correct_option="B"
)

l6 = Lesson.objects.create(
    course=c2, title="Database Design & SQL", order=3,
    thumbnail_url="https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=600&q=80",
    content="""# Database Design & SQL

Every web application needs a database. Understanding relational database design and SQL is a non-negotiable skill for full-stack developers.

## Relational Database Concepts

- **Table** — A collection of related data (like a spreadsheet)
- **Row** — A single record (one user, one order)
- **Column** — An attribute (name, email, created_at)
- **Primary Key (PK)** — Unique identifier for each row
- **Foreign Key (FK)** — Links one table to another

## Designing a Schema

Consider an e-commerce system:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    ordered_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
```

## Essential SQL Queries

```sql
-- Select with filtering
SELECT * FROM users WHERE created_at > '2024-01-01';

-- Join tables
SELECT u.username, o.total, o.status
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'completed';

-- Aggregation
SELECT user_id, COUNT(*) as order_count, SUM(total) as total_spent
FROM orders
GROUP BY user_id
HAVING SUM(total) > 1000
ORDER BY total_spent DESC;

-- Subqueries
SELECT * FROM products
WHERE id NOT IN (
    SELECT DISTINCT product_id FROM order_items
);
```

## Normalization Rules

- **1NF** — No repeating groups, atomic values
- **2NF** — 1NF + no partial dependencies
- **3NF** — 2NF + no transitive dependencies

## Indexing for Performance

```sql
-- Speed up searches on frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user ON orders(user_id);
```

Indexes make reads faster but slow down writes. Index strategically."""
)

Quiz.objects.create(
    lesson=l6,
    question="What is the purpose of a Foreign Key in a relational database?",
    option_a="To encrypt sensitive data",
    option_b="To create a unique identifier for each row",
    option_c="To link one table to another by referencing a primary key",
    option_d="To automatically delete duplicate records",
    correct_option="C"
)

# ═══════════════════════════════════════════════════
# COURSE 3: UI/UX Design Principles
# ═══════════════════════════════════════════════════
c3 = Course.objects.create(
    title="UI/UX Design Principles",
    description="Learn the psychology, principles, and practical techniques behind beautiful, intuitive user interfaces. From wireframes to high-fidelity prototypes.",
    thumbnail_url="https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800&q=80",
    icon_emoji="🎨"
)

l7 = Lesson.objects.create(
    course=c3, title="Visual Hierarchy & Layout", order=1,
    thumbnail_url="https://images.unsplash.com/photo-1545235617-7a424c1a60cc?w=600&q=80",
    content="""# Visual Hierarchy & Layout

Visual hierarchy is the arrangement of design elements in order of importance. It guides the user's eye through content naturally, ensuring they see the most important information first.

## The F-Pattern & Z-Pattern

Research shows users scan web pages in predictable patterns:

**F-Pattern** (for text-heavy pages):
1. Read across the top (header/navigation)
2. Scan down the left side
3. Read horizontally again at subheadings

**Z-Pattern** (for minimal/landing pages):
1. Top-left → Top-right
2. Diagonal to bottom-left
3. Bottom-left → Bottom-right (CTA button)

## Tools for Creating Hierarchy

### 1. Size
Larger elements draw attention first. Headlines > subheadings > body text.

### 2. Color & Contrast
High-contrast elements pop. Use a bold accent color for primary CTAs.

### 3. Whitespace (Negative Space)
Space around elements increases their perceived importance. Apple is the master of this technique.

### 4. Typography Weight
**Bold text** commands more attention than regular weight.

### 5. Position
Elements at the top-left of a page are seen first in LTR languages.

## The 60-30-10 Rule

A color distribution guideline from interior design:
- **60%** — Dominant color (background, large surfaces)
- **30%** — Secondary color (cards, sections, sidebars)
- **10%** — Accent color (CTAs, highlights, links)

## Grid Systems

Use grids for consistent, aligned layouts:

- **4-column grid** — Mobile layouts
- **8-column grid** — Tablet layouts
- **12-column grid** — Desktop layouts (most common)

Consistent spacing (multiples of 4px or 8px) creates rhythm and harmony.

## Gestalt Principles

- **Proximity** — Related elements should be close together
- **Similarity** — Similar-looking elements are perceived as related
- **Closure** — The brain fills in missing parts of shapes
- **Continuity** — The eye follows smooth paths and lines

Great design is invisible — users should never have to think about where to look."""
)

Quiz.objects.create(
    lesson=l7,
    question="According to the 60-30-10 rule, what percentage of the design should be the accent color?",
    option_a="60%",
    option_b="30%",
    option_c="10%",
    option_d="50%",
    correct_option="C"
)

l8 = Lesson.objects.create(
    course=c3, title="Color Theory for Digital Design", order=2,
    thumbnail_url="https://images.unsplash.com/photo-1525909002-1b05e0c869d8?w=600&q=80",
    content="""# Color Theory for Digital Design

Color is the most powerful tool in a designer's toolkit. It evokes emotions, communicates brand identity, and guides user behavior — all in milliseconds.

## The Color Wheel

### Primary Colors
Red, Blue, Yellow — the foundation of all colors.

### Color Harmonies

- **Complementary** — Opposite on the wheel (blue ↔ orange). High contrast, vibrant.
- **Analogous** — Adjacent colors (blue, blue-green, green). Harmonious, calming.
- **Triadic** — Three equidistant colors (red, yellow, blue). Balanced, vibrant.
- **Split-Complementary** — Base + two adjacent to complement. Less tension than complementary.

## Color Psychology

| Color | Emotion | Brands |
|-------|---------|--------|
| **Blue** | Trust, stability, calm | Facebook, IBM, PayPal |
| **Red** | Energy, urgency, passion | YouTube, Netflix, Coca-Cola |
| **Green** | Growth, health, nature | Spotify, WhatsApp, Whole Foods |
| **Yellow** | Optimism, warmth, attention | Snapchat, IKEA, McDonald's |
| **Purple** | Luxury, creativity, wisdom | Twitch, Cadbury, Hallmark |
| **Orange** | Friendly, playful, confident | Amazon, Fanta, Firefox |
| **Black** | Sophistication, power, elegance | Apple, Chanel, Nike |

## Accessibility & Contrast

WCAG guidelines require minimum contrast ratios:
- **Normal text**: 4.5:1 ratio (AA standard)
- **Large text**: 3:1 ratio (AA standard)
- **Enhanced**: 7:1 ratio (AAA standard)

Tools to check contrast:
- WebAIM Contrast Checker
- Stark (Figma plugin)
- Chrome DevTools Accessibility audit

## Building a Color System

```css
:root {
    /* Primary palette */
    --primary-50:  #eef2ff;
    --primary-100: #e0e7ff;
    --primary-500: #6366f1;  /* Main brand color */
    --primary-600: #4f46e5;
    --primary-900: #312e81;
    
    /* Semantic colors */
    --success: #10b981;
    --warning: #f59e0b;
    --error:   #ef4444;
    --info:    #3b82f6;
    
    /* Neutrals */
    --gray-50:  #f9fafb;
    --gray-900: #111827;
}
```

**Rule of thumb**: Choose one primary color, one accent, and build a range of neutrals. Test everything in both light and dark modes.

Never rely on color alone to convey meaning — always pair with icons, text, or patterns for accessibility."""
)

Quiz.objects.create(
    lesson=l8,
    question="Which color harmony uses colors that are opposite each other on the color wheel?",
    option_a="Analogous",
    option_b="Triadic",
    option_c="Complementary",
    option_d="Monochromatic",
    correct_option="C"
)

# ═══════════════════════════════════════════════════
# COURSE 4: Cybersecurity Essentials
# ═══════════════════════════════════════════════════
c4 = Course.objects.create(
    title="Cybersecurity Essentials",
    description="Understand the threat landscape, learn to think like an attacker, and build secure systems. Covers encryption, authentication, OWASP Top 10, and secure coding practices.",
    thumbnail_url="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80",
    icon_emoji="🔒"
)

l9 = Lesson.objects.create(
    course=c4, title="Cryptography Fundamentals", order=1,
    thumbnail_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&q=80",
    content="""# Cryptography Fundamentals

Cryptography is the science of securing communication in the presence of adversaries. It's the backbone of internet security — from HTTPS to cryptocurrency.

## Symmetric Encryption

The **same key** is used for both encryption and decryption.

**Common Algorithms:**
- **AES-256** — The gold standard. Used by governments, banks, and VPNs.
- **ChaCha20** — Faster on mobile devices. Used by Google and WireGuard.

```python
from cryptography.fernet import Fernet

# Generate key
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
plaintext = b"Secret message"
encrypted = cipher.encrypt(plaintext)

# Decrypt
decrypted = cipher.decrypt(encrypted)
print(decrypted)  # b"Secret message"
```

**Problem:** How do you securely share the key? This is the **key distribution problem**.

## Asymmetric Encryption (Public Key)

Uses a **key pair**: a public key (shared openly) and a private key (kept secret).

- **RSA** — The classic. Based on factoring large primes.
- **ECDSA** — Shorter keys, same security. Used in Bitcoin and TLS.
- **Ed25519** — Modern, fast. Used in SSH and Signal.

**How it works:**
1. Alice encrypts with Bob's **public key**
2. Only Bob can decrypt with his **private key**

## Hashing

One-way function: input → fixed-size output (digest). **Cannot be reversed.**

| Algorithm | Output Size | Use Case | Secure? |
|-----------|------------|----------|---------|
| MD5 | 128 bits | Checksums | ❌ Broken |
| SHA-1 | 160 bits | Legacy | ❌ Broken |
| SHA-256 | 256 bits | Blockchain, TLS | ✅ |
| bcrypt | 184 bits | Password storage | ✅ |
| Argon2 | Variable | Password storage | ✅ Best |

**Never store passwords in plain text.** Always use bcrypt or Argon2.

## Digital Signatures

Prove that a message was sent by the claimed sender and hasn't been tampered with:

1. Sender hashes the message
2. Sender encrypts the hash with their **private key** (= signature)
3. Receiver decrypts with sender's **public key**
4. Receiver hashes the message independently
5. If hashes match → message is authentic and unaltered

## TLS (Transport Layer Security)

The protocol that puts the 'S' in HTTPS:

1. **Client Hello** — Browser sends supported ciphers
2. **Server Hello** — Server picks cipher, sends certificate
3. **Key Exchange** — Establish shared secret (Diffie-Hellman)
4. **Encrypted Communication** — All data encrypted with symmetric key

Every time you see the 🔒 in your browser, TLS is working."""
)

Quiz.objects.create(
    lesson=l9,
    question="What is the fundamental problem with symmetric encryption?",
    option_a="It's too slow for modern computers",
    option_b="The key distribution problem — securely sharing the same key",
    option_c="It cannot encrypt large files",
    option_d="It requires quantum computers to work",
    correct_option="B"
)

l10 = Lesson.objects.create(
    course=c4, title="OWASP Top 10 Vulnerabilities", order=2,
    thumbnail_url="https://images.unsplash.com/photo-1563986768609-322da13575f2?w=600&q=80",
    content="""# OWASP Top 10 Vulnerabilities

The OWASP (Open Web Application Security Project) Top 10 is the definitive list of the most critical web application security risks. Every developer should understand and defend against these.

## 1. Broken Access Control

Users can access data or perform actions beyond their permissions.

```python
# ❌ VULNERABLE — No authorization check
@app.route('/api/users/<id>')
def get_user(id):
    return User.query.get(id).to_dict()

# ✅ SECURE — Verify ownership
@app.route('/api/users/<id>')
@login_required
def get_user(id):
    user = User.query.get(id)
    if user.id != current_user.id and not current_user.is_admin:
        abort(403)
    return user.to_dict()
```

## 2. Cryptographic Failures

Exposing sensitive data through weak or missing encryption.

**Rules:**
- Encrypt all data in transit (TLS/HTTPS)
- Hash passwords with bcrypt/Argon2 (never MD5/SHA-1)
- Never hardcode API keys or secrets in source code
- Use environment variables for sensitive configuration

## 3. Injection (SQL, NoSQL, OS, LDAP)

Untrusted data sent to an interpreter as part of a command.

```python
# ❌ SQL INJECTION VULNERABLE
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# ✅ PARAMETERIZED QUERY — Safe
cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))
```

## 4. Insecure Design

Flaws in the architecture itself. No amount of implementation can fix bad design.

- Threat modeling during design phase
- Use security design patterns
- Implement defense in depth

## 5. Security Misconfiguration

Default passwords, unnecessary features, overly permissive CORS, verbose error messages.

**Checklist:**
- Change all default credentials
- Disable debug mode in production
- Remove unnecessary endpoints
- Set proper CORS headers
- Keep all software updated

## 6. Vulnerable & Outdated Components

Using libraries with known security vulnerabilities.

```bash
# Check for known vulnerabilities
pip audit           # Python
npm audit           # JavaScript
snyk test           # Multi-language
```

## 7. Authentication Failures

- Weak password policies
- Missing rate limiting (brute force)
- Credentials in URLs
- Missing multi-factor authentication

## 8. Software & Data Integrity Failures

- Unsigned updates
- Insecure CI/CD pipelines
- Deserialization of untrusted data

## 9. Security Logging & Monitoring Failures

If you can't see attacks, you can't stop them.

## 10. Server-Side Request Forgery (SSRF)

The server is tricked into making requests to internal resources.

**Know these vulnerabilities inside and out.** Security is everyone's responsibility."""
)

Quiz.objects.create(
    lesson=l10,
    question="Which OWASP Top 10 vulnerability involves untrusted data being sent to an interpreter as part of a command?",
    option_a="Broken Access Control",
    option_b="Cross-Site Scripting (XSS)",
    option_c="Injection",
    option_d="Security Misconfiguration",
    correct_option="C"
)

print(f"✅ Seeded {Course.objects.count()} courses, {Lesson.objects.count()} lessons, {Quiz.objects.count()} quizzes")
