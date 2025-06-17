# --- START OF FILE tasks/design_tasks.py (Phiên bản Hoàn chỉnh 100%) ---

from crewai import Task
from textwrap import dedent
from utils.file_writer import write_output
from memory.shared_memory import shared_memory
from tasks.quality_gate_tasks import create_quality_gate_task

class DesignTasksFactory:
    """
    Nhà máy chứa tất cả các phương thức để tạo ra các task chuyên môn chi tiết
    cho Giai đoạn 3: Thiết kế Kỹ thuật.
    """

    # === architecture_tasks.py ===
    def create_architecture_tasks(self, agent) -> list[Task]:
        srs_document = shared_memory.get("phase_2", "srs_document") or "Tài liệu SRS không có sẵn."
        architecture_document = shared_memory.get("phase_3", "architecture_document") or "Tài liệu kiến trúc không có sẵn."
        task1 = Task(
            description=dedent(f"""
                # NHIỆM VỤ (1/2): XÂY DỰNG TÀI LIỆU KIẾN TRÚC HỆ THỐNG

                ## Mục tiêu:
                Dựa vào tài liệu SRS, hãy xây dựng một tài liệu kiến trúc hệ thống chi tiết, làm nền tảng cho việc phát triển.

                ## Hướng dẫn chi tiết:
                Với vai trò là một Kiến trúc sư Hệ thống, bạn cần phân tích các yêu cầu chức năng và phi chức năng trong SRS để đưa ra các quyết định thiết kế quan trọng.

                ## Yêu cầu về Cấu trúc Tài liệu:
                Tài liệu PHẢI bao gồm các phần chính sau:
                1.  **Lựa chọn Kiến trúc (Architectural Pattern)**: Đề xuất một mẫu kiến trúc (ví dụ: Microservices, Monolithic, Serverless) và giải thích lý do lựa chọn dựa trên yêu cầu về khả năng mở rộng, bảo trì, và hiệu suất.
                2.  **Sơ đồ Kiến trúc Cấp cao**: Tạo một sơ đồ bằng cú pháp **Mermaid.js** để minh họa các thành phần chính (ví dụ: Web Server, Application Server, Database, Message Queue, Caching Layer) và luồng dữ liệu giữa chúng.
                3.  **Lựa chọn Công nghệ (Technology Stack)**: Đề xuất một bộ công nghệ cụ thể cho Backend (ngôn ngữ, framework), Frontend (framework), Cơ sở dữ liệu, và các dịch vụ quan trọng khác.
                4.  **Cân nhắc về Yêu cầu Phi chức năng**: Mô tả ngắn gọn cách kiến trúc này giải quyết các NFRs quan trọng như Bảo mật, Hiệu suất, và Tính khả dụng.

                ## Tài liệu tham khảo đầu vào (SRS):
                ```markdown
                {srs_document[:2000]}...
                ```
            """),
            expected_output="""Một tài liệu kiến trúc hệ thống hoàn chỉnh, được định dạng bằng Markdown.
                Tài liệu phải có đầy đủ 4 phần đã yêu cầu, với các giải thích logic và một khối mã Mermaid.js cho sơ đồ kiến trúc.
            """,
            agent=agent,
            callback=lambda o: (
                write_output("3_design/System_Architecture.md", str(o)), 
                shared_memory.set("phase_3", "architecture_document", str(o)))
        )
        task2 = Task(
            description=dedent(f"""
                # NHIỆM VỤ (2/2): LẬP WEBSITE PLANNING CHECKLIST

                ## Mục tiêu:
                Dựa trên SRS và tài liệu kiến trúc vừa được tạo, hãy lập một Website Planning Checklist để hỗ trợ việc thiết kế và phối hợp giữa đội ngũ frontend và backend.

                ## Hướng dẫn chi tiết:
                Checklist này giúp đảm bảo tất cả các trang, thành phần, và luồng tương tác cần thiết đều được xem xét.
                Hãy phân tích các chức năng trong SRS và ánh xạ chúng vào các trang/màn hình cụ thể.

                ## Yêu cầu về Định dạng Đầu ra:
                Bạn PHẢI tạo ra một checklist dưới dạng **Bảng Markdown (Markdown Table)**.
                Bảng phải có các cột sau:
                - `ID`: Mã định danh duy nhất (ví dụ: WP-01).
                - `Trang / Thành phần (Page / Component)`: Tên của trang hoặc thành phần UI (ví dụ: Trang chủ, Form đăng nhập, Header).
                - `Mô tả Chức năng chính (Key Functionality)`: Mô tả ngắn gọn chức năng của trang/thành phần đó.
                - `API Endpoints Liên quan (Related APIs)`: Liệt kê các API endpoints dự kiến cần thiết. Điền "N/A" nếu không có.
                - `Ghi chú Kỹ thuật (Technical Notes)`: Các lưu ý đặc biệt (ví dụ: "Cần tải lazy-load", "Sử dụng WebSocket").

                ## Tài liệu tham khảo đầu vào:
                - **Tài liệu SRS (Trích đoạn)**:
                  ```markdown
                  {srs_document[:1500]}...
                  ```
                - **Tài liệu Kiến trúc (Trích đoạn)**:
                  ```markdown
                  {architecture_document[:1000]}...
                  ```
            """),
            expected_output="""Một file văn bản chứa một Bảng Markdown chi tiết.
                Bảng này là checklist lập kế hoạch website, tuân thủ 5 cột đã yêu cầu.
                Ví dụ mẫu:
                | ID    | Trang / Thành phần (Page / Component) | Mô tả Chức năng chính (Key Functionality)        | API Endpoints Liên quan (Related APIs) | Ghi chú Kỹ thuật (Technical Notes)      |
                |-------|---------------------------------------|--------------------------------------------------|---------------------------------------|-----------------------------------------|
                | WP-01 | Trang Chi tiết Sản phẩm               | Hiển thị thông tin, hình ảnh, giá của sản phẩm.  | GET /api/products/{id}                | Tải ảnh với lazy-load. Cache dữ liệu. |
                | WP-02 | Form Đăng nhập                        | Cho phép người dùng xác thực vào hệ thống.       | POST /api/auth/login                  | Cần có validation ở phía client.       |
            """,
            agent=agent, context=[task1],
            callback=lambda o: (
                write_output("3_design/Website_Planning_Checklist.md", str(o)),
                shared_memory.set("phase_3", "website_planning_checklist", str(o))
                )
        )
        return [task1, task2]

    # === dfd_tasks.py ===
    def create_dfd_task(self, agent) -> Task:
        srs_document = shared_memory.get("phase_2", "srs_document") or "Tài liệu SRS không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: XÂY DỰNG SƠ ĐỒ LUỒNG DỮ LIỆU (DFD) VÀ MÔ TẢ CHI TIẾT

                ## Mục tiêu:
                Từ tài liệu SRS, hãy xây dựng một sơ đồ luồng dữ liệu (DFD) cấp 0 (Context Diagram) và mô tả chi tiết các thành phần của sơ đồ đó.

                ## Hướng dẫn chi tiết:
                Với vai trò là một Kiến trúc sư Hệ thống, bạn cần thực hiện các bước sau:
                1.  **Xác định các thành phần DFD**: Đọc kỹ SRS để xác định:
                    - **Thực thể ngoài (External Entities)**: Người dùng, các hệ thống bên ngoài tương tác với hệ thống của bạn.
                    - **Tiến trình (Processes)**: Các hoạt động chính mà hệ thống thực hiện để xử lý dữ liệu. Ở Cấp 0, thường chỉ có một tiến trình trung tâm đại diện cho toàn bộ hệ thống.
                    - **Kho dữ liệu (Data Stores)**: Nơi dữ liệu được lưu trữ (ví dụ: CSDL người dùng, CSDL sản phẩm).
                2.  **Xác định Luồng dữ liệu**: Xác định dữ liệu nào di chuyển giữa các thành phần trên (ví dụ: "Thông tin đăng nhập", "Dữ liệu đơn hàng").
                3.  **Xây dựng Sơ đồ**: Tạo ra mã code để vẽ sơ đồ DFD bằng cú pháp **Mermaid.js**. Đây là phiên bản văn bản của sơ đồ, có thể được render thành hình ảnh.
                4.  **Viết Mô tả**: Viết mô tả chi tiết cho từng thành phần đã xác định trong bước 1.

                ## Yêu cầu về Định dạng Đầu ra:
                Bạn PHẢI tạo ra một tài liệu Markdown duy nhất, có 2 phần RÕ RÀNG:
                
                **Phần 1: Sơ đồ Luồng Dữ liệu (DFD) - Cấp 0:**
                Bắt đầu bằng tiêu đề `### Sơ đồ Luồng Dữ liệu (DFD) - Cấp 0` và theo sau là một khối code Mermaid.
                - Dùng hình chữ nhật cho Thực thể ngoài: `id[Tên]`
                - Dùng hình tròn cho Tiến trình: `id((Tên))`
                - Dùng hình database cho Kho dữ liệu: `id[(Tên)]`
                - Dùng mũi tên với nhãn để chỉ luồng dữ liệu: `A -- Luồng dữ liệu --> B`

                **Phần 2: Mô tả Chi tiết các Thành phần:**
                Bắt đầu bằng tiêu đề `### Mô tả Chi tiết các Thành phần` và có các tiểu mục cho:
                - **Thực thể ngoài (External Entities)**
                - **Tiến trình (Processes)**
                - **Kho dữ liệu (Data Stores)**

                ## Tài liệu tham khảo đầu vào (SRS):
                ```markdown
                {srs_document[:2500]}...
                ```
            """),
            expected_output="""Một file văn bản duy nhất được định dạng bằng Markdown, chứa hai phần rõ ràng.
                Phần 1 là một khối code Mermaid.js để vẽ sơ đồ DFD cấp 0.
                Phần 2 là mô tả chi tiết về các Thực thể ngoài, Tiến trình, và Kho dữ liệu đã được xác định.
                Ví dụ mẫu:
                ### Sơ đồ Luồng Dữ liệu (DFD) - Cấp 0
                ```mermaid
                graph TD
                    A[Khách hàng] -- Yêu cầu mua hàng --> B((Hệ thống Bán hàng SuperCart));
                    B -- Thông tin đơn hàng --> C[(CSDL Đơn hàng)];
                    B -- Yêu cầu thanh toán --> D[Hệ thống Thanh toán];
                    D -- Xác nhận thanh toán --> B;
                    E[Quản trị viên] -- Yêu cầu quản lý --> B;
                    C -- Dữ liệu báo cáo --> B;
                Mô tả Chi tiết các Thành phần
                1. Thực thể ngoài (External Entities):
                Khách hàng: Người dùng cuối thực hiện mua sắm trên hệ thống. Cung cấp thông tin cá nhân và yêu cầu mua hàng.
                Hệ thống Thanh toán: Đối tác bên thứ ba xử lý các giao dịch tài chính. Nhận yêu cầu thanh toán và trả về kết quả.
                Quản trị viên: Người quản lý hệ thống, sản phẩm và đơn hàng. Cung cấp các yêu cầu quản lý.
                2. Tiến trình (Processes):
                Hệ thống Bán hàng SuperCart: Tiến trình trung tâm, xử lý tất cả các yêu cầu từ người dùng và quản trị viên, tương tác với các kho dữ liệu và hệ thống ngoài.
                3. Kho dữ liệu (Data Stores):
                CSDL Đơn hàng: Nơi lưu trữ thông tin về tất cả các đơn hàng đã được tạo.
            """,
            agent=agent,
            callback=lambda o: (
                write_output("3_design/DFD_and_Description.md", str(o)), 
                shared_memory.set("phase_3", "dfd_document", str(o)))
        )

    # === db_tasks.py ===
    def create_db_task(self, agent) -> Task:
        use_case_data = shared_memory.get("phase_2", "use_cases_and_user_stories") or "Dữ liệu Use Case không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: TẠO DATABASE DESIGN DOCUMENT

                ## Mục tiêu:
                Dựa trên Use Case Diagram và User Stories đã được cung cấp, hãy xác định các thực thể dữ liệu chính và tạo ra một Database Design Document chi tiết, bao gồm định nghĩa các bảng, cột, khóa chính, và các liên kết (khóa ngoại).

                ## Hướng dẫn chi tiết:
                Với vai trò là một Kiến trúc sư Hệ thống, bạn cần thực hiện các bước sau:
                1.  **Phân tích Use Cases/User Stories**: Đọc kỹ tài liệu để xác định các "danh từ" chính. Các danh từ này thường là ứng cử viên cho các thực thể (bảng) trong CSDL (ví dụ: User, Product, Order, Cart, Payment).
                2.  **Định nghĩa Bảng (Tables)**: Với mỗi thực thể, tạo một bảng.
                3.  **Định nghĩa Cột (Columns)**: Với mỗi bảng, liệt kê các cột cần thiết, bao gồm:
                    - Tên cột (ví dụ: `user_id`, `product_name`, `order_date`).
                    - Kiểu dữ liệu (ví dụ: `INT`, `VARCHAR(255)`, `TEXT`, `DECIMAL(10, 2)`, `TIMESTAMP`).
                    - Các ràng buộc (ví dụ: `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`).
                4.  **Xác định Liên kết (Relationships)**: Sử dụng Khóa ngoại (FOREIGN KEY) để thể hiện mối quan hệ giữa các bảng (ví dụ: một `Order` phải thuộc về một `User`).

                ## Yêu cầu về Định dạng Đầu ra:
                Bạn PHẢI tạo ra một tài liệu Markdown duy nhất. Trong tài liệu này, **mỗi bảng trong cơ sở dữ liệu được mô tả bằng một Bảng Markdown (Markdown Table)**.
                - Bảng Markdown này phải có các cột: `Tên cột (Column Name)`, `Kiểu dữ liệu (Data Type)`, `Ràng buộc (Constraints)`, và `Mô tả (Description)`.

                ## Tài liệu tham khảo đầu vào (Use Cases & User Stories):
                ```markdown
                {use_case_data[:2000]}...
                ```
            """),
            expected_output="""Một tài liệu Markdown chi tiết mô tả thiết kế cơ sở dữ liệu.
                Tài liệu phải chứa nhiều Bảng Markdown, mỗi bảng tương ứng với một bảng trong CSDL và có đầy đủ 4 cột như yêu cầu.
                Ví dụ mẫu:
                # Database Design Document

                ### Bảng: Users
                | Tên cột (Column Name) | Kiểu dữ liệu (Data Type) | Ràng buộc (Constraints)        | Mô tả (Description)                      |
                |------------------------|---------------------------|---------------------------------|------------------------------------------|
                | user_id                | INT                       | PRIMARY KEY, AUTO_INCREMENT     | Mã định danh duy nhất cho người dùng.     |
                | username               | VARCHAR(50)               | UNIQUE, NOT NULL                | Tên đăng nhập của người dùng.            |
                | email                  | VARCHAR(100)              | UNIQUE, NOT NULL                | Địa chỉ email của người dùng.            |
                | password_hash          | VARCHAR(255)              | NOT NULL                        | Mật khẩu đã được băm.                    |
                | created_at             | TIMESTAMP                 | DEFAULT CURRENT_TIMESTAMP       | Thời gian tài khoản được tạo.            |

                ### Bảng: Orders
                | Tên cột (Column Name) | Kiểu dữ liệu (Data Type) | Ràng buộc (Constraints)        | Mô tả (Description)                      |
                |------------------------|---------------------------|---------------------------------|------------------------------------------|
                | order_id               | INT                       | PRIMARY KEY, AUTO_INCREMENT     | Mã định danh duy nhất cho đơn hàng.      |
                | user_id                | INT                       | FOREIGN KEY (Users.user_id)     | Liên kết đến người dùng đã đặt hàng.   |
                | total_amount           | DECIMAL(10, 2)            | NOT NULL                        | Tổng giá trị đơn hàng.                   |
                | status                 | VARCHAR(50)               | NOT NULL                        | Trạng thái đơn hàng (e.g., pending).   |
                | order_date             | TIMESTAMP                 | DEFAULT CURRENT_TIMESTAMP       | Thời gian đơn hàng được tạo.             |
            """,
            agent=agent,
            callback=lambda o: (
                write_output("3_design/Database_Design_Document.md", str(o)), 
                shared_memory.set("phase_3", "database_design_document", str(o))
                )
        )

    # === api_tasks.py ===
    def create_api_task(self, agent) -> Task:
        srs_document = shared_memory.get("phase_2", "srs_document") or "Tài liệu SRS không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: TẠO API DESIGN DOCUMENT (CHUẨN OPENAPI 3.0)

                ## Mục tiêu:
                Phân tích tài liệu SRS và tạo ra một API Design Document chi tiết dưới định dạng YAML, tuân thủ nghiêm ngặt đặc tả OpenAPI 3.0.0.

                ## Hướng dẫn chi tiết:
                Với vai trò là một Kiến trúc sư Hệ thống, bạn hãy phân tích các yêu cầu chức năng trong SRS để xác định các "tài nguyên" (resources) chính của hệ thống (ví dụ: users, products, orders). Sau đó, định nghĩa các hoạt động CRUD (Create, Read, Update, Delete) trên các tài nguyên đó dưới dạng các API endpoint.

                ## Yêu cầu về Định dạng Đầu ra:
                Toàn bộ kết quả của bạn PHẢI là một chuỗi văn bản duy nhất, là một file YAML hợp lệ theo chuẩn OpenAPI 3.0.0.
                File YAML phải có cấu trúc cơ bản như sau:
                - `openapi: 3.0.0`
                - `info`: Chứa thông tin về API (title, version).
                - `servers`: Chứa URL của server.
                - `paths`: Đây là phần chính, định nghĩa tất cả các endpoints.
                    - Với mỗi path (ví dụ: `/products`), định nghĩa các phương thức HTTP (get, post, ...).
                    - Với mỗi phương thức, định nghĩa `summary`, `parameters` (nếu có), `requestBody` (cho POST/PUT), và `responses`.
                - `components/schemas`: Định nghĩa các mô hình dữ liệu (data models) được sử dụng lại trong `requestBody` và `responses`.

                ## Tài liệu tham khảo đầu vào (SRS):
                ```markdown
                {srs_document[:3000]}...
            ```
            """),
            expected_output="""Một chuỗi văn bản duy nhất là một file YAML hợp lệ, tuân thủ đầy đủ đặc tả OpenAPI 3.0.0.
                Ví dụ mẫu:
                ```yaml
                openapi: 3.0.0
                info:
                title: SuperCart API
                version: 1.0.0
                description: API for the SuperCart E-commerce platform.
                servers:
                - url: https://api.supercart.com/v1
                paths:
                /products:
                    get:
                    summary: Get a list of all products
                    responses:
                        '200':
                        description: A list of products.
                        content:
                            application/json:
                            schema:
                                type: array
                                items:
                                $ref: '#/components/schemas/Product'
                /products/{productId}:
                    get:
                    summary: Get a single product by ID
                    parameters:
                        - name: productId
                        in: path
                        required: true
                        schema:
                            type: integer
                    responses:
                        '200':
                        description: A single product.
                        content:
                            application/json:
                            schema:
                                $ref: '#/components/schemas/Product'
                        '404':
                        description: Product not found.
                components:
                schemas:
                    Product:
                    type: object
                    properties:
                        id:
                        type: integer
                        example: 1
                        name:
                        type: string
                        example: "Laptop Pro"
                        price:
                        type: number
                        format: float
                        example: 1200.50
            """,
            agent=agent,
            callback=lambda o: (
                write_output("3_design/API_Design_Document.yaml", str(o)), 
                shared_memory.set("phase_3", "api_design_document", str(o)))
        )

    # === security_arch_tasks.py ===
    def create_security_arch_task(self, agent) -> Task:
        security_requirements_doc = shared_memory.get("phase_2", "privacy_and_security_requirements") or "Yêu cầu Bảo mật không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: TẠO TÀI LIỆU KIẾN TRÚC BẢO MẬT (SECURITY ARCHITECTURE)

                ## Mục tiêu:
                Từ các yêu cầu bảo mật và quyền riêng tư đã được xác định, hãy thiết kế và tạo một tài liệu Security Architecture chi tiết, mô tả các cơ chế, công nghệ và quy trình để bảo vệ hệ thống.

                ## Hướng dẫn chi tiết:
                Với vai trò là một Kiến trúc sư Hệ thống, bạn không chỉ liệt kê lại yêu cầu, mà phải **thiết kế giải pháp** cho từng yêu cầu đó. Hãy đề xuất các công nghệ và phương pháp cụ thể.

                ## Yêu cầu về Cấu trúc Tài liệu:
                Tài liệu PHẢI bao gồm các phần chính sau, mô tả cách hệ thống sẽ được bảo vệ:
                1.  **Mô hình Đe dọa và Bề mặt Tấn công (Threat Modeling & Attack Surface)**: Phân tích các mối đe dọa tiềm tàng đối với hệ thống (ví dụ: dựa trên OWASP Top 10).
                2.  **Kiến trúc Mạng và Vành đai Bảo vệ (Network & Perimeter Security)**:
                    - Mô tả thiết lập mạng (ví dụ: sử dụng Virtual Private Cloud - VPC).
                    - Các lớp bảo vệ (ví dụ: Web Application Firewall - WAF, Network ACLs, Security Groups).
                3.  **Quản lý Định danh và Truy cập (Identity and Access Management - IAM)**:
                    - Thiết kế luồng xác thực (Authentication), đề xuất công nghệ (ví dụ: JWT, OAuth 2.0).
                    - Thiết kế luồng phân quyền (Authorization), đề xuất mô hình (ví dụ: Role-Based Access Control - RBAC).
                4.  **Bảo vệ Dữ liệu (Data Protection)**:
                    - Cơ chế mã hóa dữ liệu khi lưu trữ (Encryption at Rest), ví dụ: TDE của CSDL, mã hóa cấp ứng dụng.
                    - Cơ chế mã hóa dữ liệu khi truyền (Encryption in Transit), ví dụ: Bắt buộc sử dụng TLS 1.2/1.3 (HTTPS).
                5.  **Bảo mật Ứng dụng (Application Security)**:
                    - Các biện pháp phòng chống tấn công phổ biến (ví dụ: Input Validation để chống SQL Injection/XSS, sử dụng prepared statements).
                    - Quản lý và quét các thư viện phụ thuộc (Dependency Management).
                6.  **Ghi nhật ký và Giám sát An ninh (Security Logging & Monitoring)**:
                    - Các sự kiện an ninh quan trọng cần ghi log.
                    - Đề xuất hệ thống giám sát và cảnh báo (ví dụ: tích hợp với SIEM).

                ## Tài liệu tham khảo đầu vào (Yêu cầu Bảo mật & Quyền riêng tư):
                ```markdown
                {security_requirements_doc[:3000]}...
                ```
            """),
            expected_output="""Một tài liệu Kiến trúc Bảo mật toàn diện, được định dạng bằng Markdown.
                Tài liệu phải có đầy đủ 6 phần đã yêu cầu, trong đó mỗi phần đều mô tả các giải pháp kỹ thuật cụ thể chứ không chỉ liệt kê lại yêu cầu.
                Ví dụ mẫu:
                # Security Architecture Document

                ### 3. Quản lý Định danh và Truy cập (IAM)
                - **Xác thực**: Sử dụng JSON Web Tokens (JWT) cho việc xác thực API. Token sẽ được ký bằng thuật toán RS256 và có thời gian hết hạn ngắn (15 phút). Refresh token sẽ được sử dụng để duy trì phiên đăng nhập.
                - **Phân quyền**: Áp dụng mô hình Role-Based Access Control (RBAC). Hệ thống sẽ định nghĩa các vai trò (User, Admin, Editor) với các quyền hạn (permissions) được gán sẵn. Middleware của API sẽ kiểm tra quyền của người dùng trước khi thực thi hành động.

                ### 4. Bảo vệ Dữ liệu (Data Protection)
                - **Encryption at Rest**: Tất cả dữ liệu nhạy cảm của người dùng (email, số điện thoại) trong cơ sở dữ liệu sẽ được mã hóa ở cấp ứng dụng trước khi lưu trữ. Cơ sở dữ liệu sẽ được bật tính năng Transparent Data Encryption (TDE).
                - **Encryption in Transit**: Toàn bộ giao tiếp giữa client và server, cũng như giữa các dịch vụ nội bộ, phải sử dụng TLS 1.3.
            """,
            agent=agent,
            callback=lambda o: (
                write_output("3_design/Security_Architecture_Document.md", str(o)), 
                shared_memory.set("phase_3", "security_architecture_document", str(o)))
        )

    # === hld_tasks.py ===
    def create_hld_task(self, agent) -> Task:
        architecture_document = shared_memory.get("phase_3", "architecture_document") or "Tài liệu Kiến trúc không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: TẠO TÀI LIỆU THIẾT KẾ CẤP CAO (HIGH-LEVEL DESIGN)

                ## Mục tiêu:
                Dựa trên tài liệu System Architecture, hãy tạo một tài liệu High-Level Design (HLD) chi tiết, phân rã hệ thống thành các thành phần/module chính, mô tả mối quan hệ và chức năng tổng quan của chúng.

                ## Hướng dẫn chi tiết:
                Với vai trò là một Kiến trúc sư Hệ thống, bạn cần cụ thể hóa bản vẽ kiến trúc thành các khối xây dựng logic. Tài liệu HLD này sẽ là cầu nối giữa kiến trúc và thiết kế chi tiết (low-level design).

                ## Yêu cầu về Cấu trúc Tài liệu:
                Tài liệu HLD PHẢI bao gồm các phần chính sau:
                1.  **Tổng quan Thiết kế (Design Overview)**: Tóm tắt lại kiến trúc đã chọn và mục tiêu của bản thiết kế này.
                2.  **Phân rã Thành phần (Component Breakdown)**:
                    - Liệt kê tất cả các module/component chính của hệ thống (ví dụ: User Service, Product Service, Order Service, API Gateway, Frontend App).
                    - Với mỗi component, mô tả ngắn gọn **trách nhiệm chính (key responsibilities)** của nó.
                3.  **Sơ đồ Tương tác Thành phần (Component Interaction Diagram)**:
                    - Tạo một sơ đồ bằng cú pháp **Mermaid.js** để minh họa cách các thành phần chính tương tác với nhau.
                    - Sơ đồ phải thể hiện được luồng gọi (ví dụ: Frontend App gọi API Gateway, API Gateway điều hướng đến các service).
                4.  **Luồng Dữ liệu Cấp cao (High-Level Data Flow)**: Mô tả cách dữ liệu di chuyển giữa các thành phần chính cho một vài kịch bản quan trọng (ví dụ: luồng xử lý một đơn hàng mới).
                5.  **Tổng kết Công nghệ (Technology Stack Summary)**: Tóm tắt lại bộ công nghệ đã được chọn cho từng thành phần.

                ## Tài liệu tham khảo đầu vào (System Architecture):
                ```markdown
                {architecture_document[:3000]}...
                ```
            """),
            expected_output="""Một tài liệu High-Level Design hoàn chỉnh, được định dạng chuyên nghiệp bằng Markdown.
                Tài liệu phải có đầy đủ 5 phần đã yêu cầu, với các mô tả rõ ràng và một sơ đồ tương tác thành phần bằng Mermaid.js.
                Ví dụ mẫu:
                # High-Level Design for SuperCart

                ### 2. Phân rã Thành phần
                - **Frontend App (React)**: Chịu trách nhiệm hiển thị giao diện người dùng và tương tác với người dùng cuối.
                - **API Gateway**: Điểm vào duy nhất cho tất cả các request từ client. Chịu trách nhiệm routing, xác thực, và rate limiting.
                - **User Service (Node.js)**: Quản lý tất cả logic liên quan đến người dùng (đăng ký, đăng nhập, hồ sơ).
                - **Product Service (Python)**: Quản lý thông tin sản phẩm và kho hàng.

                ### 3. Sơ đồ Tương tác Thành phần
                ```mermaid
                graph TD
                    A[Client/Frontend App] --> B[API Gateway];
                    B --> C[User Service];
                    B --> D[Product Service];
                    C --> E[(User DB)];
                    D --> F[(Product DB)];
                """,
            agent=agent,
            callback=lambda o: (
                write_output("3_design/High_Level_Design.md", str(o)), 
                shared_memory.set("phase_3", "high_level_design", str(o)))
        )

    # === lld_tasks.py ===
    def create_lld_task(self, agent) -> Task:
        hld_document = shared_memory.get("phase_3", "high_level_design") or "Tài liệu HLD không có sẵn."
        return Task(
           description=dedent(f"""
                # NHIỆM VỤ: PHÁT TRIỂN TÀI LIỆU THIẾT KẾ CẤP THẤP (LOW-LEVEL DESIGN)

                ## Mục tiêu:
                Từ tài liệu High-Level Design, hãy phát triển một tài liệu Low-Level Design (LLD) chi tiết cho từng module chính, bao gồm thiết kế các lớp (classes), các phương thức (methods), cấu trúc dữ liệu và logic thuật toán.

                ## Hướng dẫn chi tiết:
                Với vai trò là một Kiến trúc sư Hệ thống, bạn cần "đi sâu" vào từng component đã được xác định trong HLD. Với **mỗi module/service chính** (ví dụ: User Service, Product Service), bạn cần phải:
                1.  **Thiết kế các Lớp (Classes)**: Xác định các lớp chính trong module và mối quan hệ giữa chúng (kế thừa, tổng hợp).
                2.  **Vẽ Sơ đồ Lớp (Class Diagram)**: Tạo một sơ đồ lớp đơn giản bằng cú pháp **Mermaid.js** để minh họa các lớp và mối quan hệ của chúng.
                3.  **Đặc tả Phương thức (Methods)**: Với mỗi lớp, liệt kê các phương thức quan trọng. Với mỗi phương thức, chỉ định:
                    - Tên phương thức.
                    - Các tham số đầu vào (tên, kiểu dữ liệu).
                    - Kiểu dữ liệu trả về.
                    - Mô tả logic hoạt động dưới dạng **pseudocode** (giả mã).
                4.  **Cấu trúc Dữ liệu (Data Structures)**: Mô tả các đối tượng dữ liệu (DTOs) được sử dụng để giao tiếp giữa các lớp hoặc qua API.

                ## Yêu cầu về Cấu trúc Tài liệu:
                Tài liệu LLD PHẢI có cấu trúc phân cấp. Với mỗi module chính được tìm thấy trong HLD, tạo một phần riêng biệt.
                Mỗi phần của module phải bao gồm:
                - **Sơ đồ Lớp (Mermaid.js)**
                - **Đặc tả chi tiết các Lớp và Phương thức**

                ## Tài liệu tham khảo đầu vào (High-Level Design):
                ```markdown
                {hld_document[:3000]}...
                ```
            """),
            expected_output="""Một tài liệu Low-Level Design cực kỳ chi tiết, được định dạng bằng Markdown.
                Tài liệu phải có một phần riêng cho mỗi module/service chính.
                Mỗi phần phải chứa một sơ đồ lớp bằng Mermaid.js và đặc tả chi tiết cho từng lớp và phương thức bên trong.
                Ví dụ mẫu cho một module:
                ## Module: User Service

                ### Sơ đồ Lớp
                ```mermaid
                classDiagram
                class UserService {
                    +UserRepository repository
                    +registerUser(userData) User
                    +loginUser(credentials) string
                    +getUserProfile(userId) User
                }
                class UserRepository {
                    +findByEmail(email) User
                    +findById(userId) User
                    +save(user) User
                }
                UserService --> UserRepository
                Đặc tả Chi tiết
                Class: UserService
                Mô tả: Xử lý logic nghiệp vụ liên quan đến người dùng.
                Phương thức:
                registerUser(userData: UserDTO) -> User:
                Mô tả: Đăng ký một người dùng mới.
                Pseudocode:
                Validate userData (email không trùng, password đủ mạnh).
                If validation fails, throw exception.
                Hash the password in userData.
                Call repository.save(userData) to store user in DB.
                Return the newly created User object.
                loginUser(credentials: LoginDTO) -> string:
                Mô tả: Xác thực người dùng và trả về một JWT.
                Pseudocode:
                Call repository.findByEmail(credentials.email).
                If user not found, throw AuthenticationError.
                Compare hashed password from DB with credentials.password.
                If passwords don't match, throw AuthenticationError.
                Generate a JWT containing user_id and role.
                Return the JWT string.
            """,
            agent=agent,
            callback=lambda o: (
                write_output("3_design/Low_Level_Design.md", str(o)), 
                shared_memory.set("phase_3", "low_level_design", str(o)))
        )

    # === report_tasks.py ===
    def create_report_design_task(self, agent) -> Task:
        use_case_data = shared_memory.get("phase_2", "use_cases_and_user_stories") or "Dữ liệu Use Case không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: THIẾT KẾ MẪU BÁO CÁO CHO NGƯỜI DÙNG

                ## Mục tiêu:
                Sử dụng sơ đồ Use Case và User Stories để thiết kế một mẫu báo cáo chức năng cho người dùng (ví dụ: báo cáo doanh thu cho quản lý), bao gồm thiết kế biểu mẫu báo cáo và mô tả luồng xuất dữ liệu.

                ## Hướng dẫn chi tiết:
                Với vai trò là một Kiến trúc sư Hệ thống, bạn cần kết hợp tư duy của một nhà phân tích dữ liệu và một nhà thiết kế.
                1.  **Xác định Nhu cầu Báo cáo**: Đọc kỹ Use Cases và User Stories để tìm ra các hoạt động tạo ra dữ liệu có giá trị cần được thống kê (ví dụ: "Quản trị viên xem báo cáo doanh thu", "Người dùng xem lịch sử đơn hàng"). Chọn một loại báo cáo quan trọng nhất để thiết kế.
                2.  **Thiết kế Bố cục (Layout)**: Mô tả bố cục trực quan của báo cáo. Báo cáo sẽ có những phần nào? Sẽ có biểu đồ gì? Bảng dữ liệu nào?
                3.  **Thiết kế Biểu mẫu Đầu vào (Input Form)**: Thiết kế các bộ lọc mà người dùng có thể sử dụng để tùy chỉnh báo cáo (ví dụ: bộ lọc theo khoảng thời gian, theo trạng thái, theo danh mục sản phẩm).
                4.  **Mô tả Luồng Xuất Dữ liệu**: Mô tả các bước mà hệ thống cần thực hiện để thu thập, xử lý và hiển thị dữ liệu cho báo cáo.

                ## Yêu cầu về Cấu trúc Tài liệu Thiết kế:
                Bạn PHẢI tạo ra một tài liệu Markdown duy nhất, có các phần chính sau:
                - **1. Tên và Mục tiêu Báo cáo**: Tên của báo cáo là gì? Nó giúp người dùng giải quyết vấn đề gì?
                - **2. Đối tượng Người dùng**: Ai sẽ sử dụng báo cáo này?
                - **3. Thiết kế Bố cục và Trực quan hóa**: Mô tả chi tiết các phần của báo cáo và các loại biểu đồ được đề xuất.
                - **4. Biểu mẫu Lọc Dữ liệu (Input Parameters)**: Liệt kê các bộ lọc và tùy chọn mà người dùng có thể chọn.
                - **5. Luồng Xử lý và Xuất Dữ liệu (Data Flow)**: Mô tả từng bước logic để tạo ra báo cáo.

                ## Tài liệu tham khảo đầu vào (Use Cases & User Stories):
                ```markdown
                {use_case_data[:2000]}...
                ```
            """),
            expected_output="""Một tài liệu thiết kế mẫu báo cáo chi tiết, được định dạng bằng Markdown.
                Tài liệu phải có đầy đủ 5 phần đã yêu cầu, với các mô tả rõ ràng và thực tế.
                Ví dụ mẫu:
                # Thiết kế Mẫu báo cáo: Báo cáo Doanh thu Tháng

                ### 1. Tên và Mục tiêu Báo cáo
                - **Tên**: Báo cáo Doanh thu theo Tháng.
                - **Mục tiêu**: Cung cấp cho Quản lý một cái nhìn tổng quan về hiệu suất kinh doanh, các sản phẩm bán chạy và xu hướng doanh thu trong một khoảng thời gian nhất định.

                ### 2. Đối tượng Người dùng
                - Quản lý Kinh doanh (Sales Manager), Quản trị viên Hệ thống (Admin).

                ### 3. Thiết kế Bố cục và Trực quan hóa
                - **Phần 1: Thẻ Tóm tắt (Summary Cards)**
                - Tổng Doanh thu.
                - Tổng số Đơn hàng.
                - Giá trị Đơn hàng Trung bình.
                - **Phần 2: Biểu đồ Đường (Line Chart)**
                - Trục X: Ngày trong tháng.
                - Trục Y: Tổng doanh thu mỗi ngày.
                - **Phần 3: Bảng Dữ liệu (Data Table)**
                - Top 10 sản phẩm bán chạy nhất, với các cột: Tên sản phẩm, Số lượng đã bán, Tổng doanh thu.

                ### 4. Biểu mẫu Lọc Dữ liệu (Input Parameters)
                - **Chọn Tháng/Năm**: Dropdown để chọn tháng và năm muốn xem báo cáo.
                - **Trạng thái Đơn hàng**: Checkbox để lọc theo trạng thái (ví dụ: Hoàn thành, Đã hủy).

                ### 5. Luồng Xử lý và Xuất Dữ liệu (Data Flow)
                1.  Người dùng chọn tháng/năm và nhấn nút "Xem báo cáo".
                2.  Frontend gửi request đến API endpoint `/api/reports/sales` với tham số `month` và `year`.
                3.  Backend nhận request, truy vấn vào CSDL (bảng Orders và Order_Items) để lấy tất cả các đơn hàng trong khoảng thời gian đã cho.
                4.  Backend tổng hợp dữ liệu: tính tổng doanh thu, đếm đơn hàng, thống kê theo ngày và theo sản phẩm.
                5.  Backend trả về một đối tượng JSON chứa tất cả dữ liệu đã được xử lý.
                6.  Frontend nhận dữ liệu và render các thành phần UI (thẻ, biểu đồ, bảng).
            """,
            agent=agent,
            callback=lambda o: (
                write_output("3_design/Report_Design_Template.md", str(o))
            )
        )

    # === sequence_tasks.py ===
    def create_sequence_task(self, agent) -> Task:
        use_case_data = shared_memory.get("phase_2", "use_cases_and_user_stories") or "Dữ liệu Use Case không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: TẠO SƠ ĐỒ TRÌNH TỰ (SEQUENCE DIAGRAMS)

                ## Mục tiêu:
                Tạo các sơ đồ Sequence Diagram dựa trên tài liệu Use Cases/User Stories để mô tả chi tiết luồng thực thi giữa các thành phần hệ thống cho từng chức năng chính.

                ## Hướng dẫn chi tiết:
                Với vai trò là một Kiến trúc sư Hệ thống, bạn hãy:
                1.  **Phân tích tài liệu Use Cases/User Stories**: Đọc kỹ tài liệu để hiểu các luồng tương tác.
                2.  **Chọn các Luồng Quan trọng**: Chọn ra 2-3 luồng chức năng quan trọng nhất (ví dụ: Đăng ký người dùng, Tạo đơn hàng, Thanh toán).
                3.  **Xác định các Đối tượng tham gia (Participants)**: Với mỗi luồng, xác định các đối tượng tham gia như: `Client` (Browser/Mobile), `API Gateway`, các `Microservice` (ví dụ: `UserService`, `OrderService`), và `Database`.
                4.  **Tạo Sơ đồ cho mỗi Luồng**: Với **mỗi luồng chức năng đã chọn**, hãy tạo một sơ đồ trình tự riêng biệt bằng cú pháp **Mermaid.js**, mô tả chính xác thứ tự các thông điệp (lời gọi hàm, request API) được gửi giữa các đối tượng.

                ## Yêu cầu về Định dạng Đầu ra:
                Bạn PHẢI tạo ra một tài liệu Markdown duy nhất. Mỗi sơ đồ phải được đặt dưới một tiêu đề rõ ràng mô tả use case tương ứng, và theo sau là một khối code Mermaid.
                Sử dụng các cú pháp Mermaid như `participant`, `->>` (lời gọi đồng bộ), `-->>` (phản hồi), `activate`, `deactivate`, `alt`, `loop`.

                ## Tài liệu tham khảo đầu vào (Use Cases & User Stories):
                ```markdown
                {use_case_data[:2000]}...
                ```
            """),
            expected_output="""Một tài liệu Markdown chứa nhiều sơ đồ trình tự, mỗi sơ đồ cho một use case quan trọng.
                Mỗi sơ đồ được định dạng bằng code Mermaid.js.
                Ví dụ mẫu:
                # Sơ đồ Trình tự

                ### Use Case: Đăng ký Người dùng Mới

                ```mermaid
                sequenceDiagram
                    participant Client
                    participant API_Gateway
                    participant UserService
                    participant Database

                    activate Client
                    Client->>API_Gateway: POST /api/auth/register (userData)
                    activate API_Gateway

                    API_Gateway->>UserService: registerUser(userData)
                    activate UserService

                    UserService->>Database: check if email exists
                    activate Database
                    Database-->>UserService: email does not exist
                    deactivate Database

                    UserService->>Database: save new user
                    activate Database
                    Database-->>UserService: user created successfully
                    deactivate Database

                    UserService-->>API_Gateway: { user, token }
                    deactivate UserService

                    API_Gateway-->>Client: 201 Created { user, token }
                    deactivate API_Gateway
                    deactivate Client
                    Use Case: Xử lý Đơn hàng
                ... (sơ đồ tiếp theo ở đây) ...
            """,
            agent=agent,
            callback=lambda o: (
                write_output("3_design/Sequence_Diagrams.md", str(o))
            )
        )


def create_design_tasks(design_agent, project_manager_agent):
    """
    Hàm điều phối chính: tạo, phân công và sắp xếp tất cả các task cho Giai đoạn Thiết kế.
    """
    tasks_factory = DesignTasksFactory()
    
    architecture_tasks_list = tasks_factory.create_architecture_tasks(agent=design_agent)
    dfd_task = tasks_factory.create_dfd_task(agent=design_agent)
    db_task = tasks_factory.create_db_task(agent=design_agent)
    api_task = tasks_factory.create_api_task(agent=design_agent)
    security_arch_task = tasks_factory.create_security_arch_task(agent=design_agent)
    hld_task = tasks_factory.create_hld_task(agent=design_agent)
    lld_task = tasks_factory.create_lld_task(agent=design_agent)
    report_design_task = tasks_factory.create_report_design_task(agent=design_agent)
    sequence_task = tasks_factory.create_sequence_task(agent=design_agent)

    dfd_task.context = [architecture_tasks_list[1]]
    db_task.context = [architecture_tasks_list[1]]
    api_task.context = [architecture_tasks_list[1]]
    security_arch_task.context = [architecture_tasks_list[1]]
    hld_task.context = [architecture_tasks_list[1]]
    lld_task.context = [hld_task]
    report_design_task.context = [db_task]
    sequence_task.context = [hld_task, api_task]

    core_tasks = [
        architecture_tasks_list[0], architecture_tasks_list[1], dfd_task, db_task,
        api_task, security_arch_task, hld_task, lld_task, report_design_task, sequence_task
    ]

    quality_gate_design_task = create_quality_gate_task(
        agent=project_manager_agent,
        phase_name="Phase 3: Design",
        keys_to_check="architecture_document, database_design_document, api_design_document, high_level_design, low_level_design",
        document_names="Architecture, Database Design, API Design, HLD, LLD, and all related diagrams."
    )
    quality_gate_design_task.context = core_tasks

    return core_tasks + [quality_gate_design_task]
