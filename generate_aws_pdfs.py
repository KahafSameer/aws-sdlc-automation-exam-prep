"""
Professional AWS Topics PDF Generator
Creates beautifully designed PDF files for LinkedIn posting
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os

# AWS Brand Colors
AWS_ORANGE = HexColor('#FF9900')
AWS_DARK = HexColor('#232F3E')
AWS_LIGHT_GRAY = HexColor('#F4F4F4')
AWS_BLUE = HexColor('#146EB4')

class PDFGenerator:
    def __init__(self, output_dir="AWS_PDFs"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
    def create_custom_styles(self):
        """Create custom paragraph styles for professional look"""
        styles = getSampleStyleSheet()
        
        # Title style
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=AWS_DARK,
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=AWS_ORANGE,
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body style
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=AWS_DARK,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leading=16
        ))
        
        # Bullet style
        styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=styles['BodyText'],
            fontSize=10,
            textColor=AWS_DARK,
            leftIndent=20,
            spaceAfter=8,
            bulletIndent=10,
            leading=14
        ))
        
        return styles
    
    def add_header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()
        
        # Header - AWS branding bar
        canvas.setFillColor(AWS_ORANGE)
        canvas.rect(0, letter[1] - 0.5*inch, letter[0], 0.5*inch, fill=True, stroke=False)
        
        # Footer
        canvas.setFillColor(AWS_DARK)
        canvas.setFont('Helvetica', 9)
        footer_text = "AWS Certification Study Material | LinkedIn Post"
        canvas.drawCentredString(letter[0]/2, 0.7*inch, footer_text)
        
        # Author name
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(AWS_ORANGE)
        author_text = "Kahaf Sameer - DevOps Engineer"
        canvas.drawCentredString(letter[0]/2, 0.4*inch, author_text)
        
        # Page number
        canvas.setFillColor(AWS_DARK)
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(letter[0] - inch, 0.5*inch, f"Page {doc.page}")
        
        canvas.restoreState()
    
    def create_pdf(self, filename, title, content_sections):
        """Create a professional PDF with the given content"""
        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=1*inch, bottomMargin=1*inch)
        
        story = []
        styles = self.create_custom_styles()
        
        # Title
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(title, styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # Add a decorative line
        line_table = Table([['']], colWidths=[6.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, AWS_ORANGE),
            ('LINEBELOW', (0, 0), (-1, 0), 2, AWS_ORANGE),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Content sections
        for section in content_sections:
            if 'subtitle' in section:
                story.append(Paragraph(section['subtitle'], styles['CustomSubtitle']))
                story.append(Spacer(1, 0.1*inch))
            
            if 'text' in section:
                story.append(Paragraph(section['text'], styles['CustomBody']))
                story.append(Spacer(1, 0.15*inch))
            
            if 'bullets' in section:
                for bullet in section['bullets']:
                    bullet_text = f"• {bullet}"
                    story.append(Paragraph(bullet_text, styles['CustomBullet']))
                story.append(Spacer(1, 0.15*inch))
            
            if 'box' in section:
                # Create a highlighted box for key information
                box_data = [[Paragraph(section['box'], styles['CustomBody'])]]
                box_table = Table(box_data, colWidths=[6*inch])
                box_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), AWS_LIGHT_GRAY),
                    ('BOX', (0, 0), (-1, -1), 2, AWS_BLUE),
                    ('LEFTPADDING', (0, 0), (-1, -1), 12),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ]))
                story.append(box_table)
                story.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(story, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)
        print(f"✓ Created: {filename}")

def main():
    generator = PDFGenerator()
    
    # 1. Continuous Integration
    generator.create_pdf(
        "01_Continuous_Integration.pdf",
        "What is Continuous Integration?",
        [
            {
                'subtitle': 'Overview',
                'text': 'Continuous Integration (CI) is a software development practice where developers regularly merge their code changes into a central repository, after which automated builds and tests are run. The key goals are to find and address bugs quicker, improve software quality, and reduce the time it takes to validate and release new software updates.'
            },
            {
                'subtitle': 'Key Benefits',
                'bullets': [
                    '<b>Early Bug Detection:</b> Automated testing catches integration errors quickly',
                    '<b>Reduced Integration Risk:</b> Frequent merges prevent complex conflicts',
                    '<b>Faster Development:</b> Automated workflows accelerate the development cycle',
                    '<b>Improved Code Quality:</b> Consistent testing ensures higher standards',
                    '<b>Better Collaboration:</b> Teams stay synchronized with frequent updates'
                ]
            },
            {
                'subtitle': 'AWS CI Best Practices',
                'bullets': [
                    'Automate everything possible using AWS CodeBuild and CodePipeline',
                    'Implement robust version control with AWS CodeCommit',
                    'Use Infrastructure as Code with AWS CloudFormation',
                    'Integrate comprehensive automated testing at every stage',
                    'Store secrets securely using AWS Secrets Manager',
                    'Enable continuous monitoring with Amazon CloudWatch',
                    'Commit and merge code changes frequently',
                    'Isolate environments with separate AWS accounts'
                ]
            },
            {
                'box': '<b>AWS CI/CD Services:</b> AWS CodePipeline orchestrates the entire CI/CD workflow, AWS CodeBuild handles continuous integration and testing, AWS CodeCommit provides source control, and AWS CodeDeploy automates deployments.'
            }
        ]
    )
    
    # 2. Continuous Delivery
    generator.create_pdf(
        "02_Continuous_Delivery.pdf",
        "What is Continuous Delivery?",
        [
            {
                'subtitle': 'Overview',
                'text': 'Continuous Delivery (CD) is a software engineering approach that ensures code can be reliably released at any time. It automates the release process, preparing every code change for deployment to testing or staging environments after the build stage, typically with a manual approval step before production deployment.'
            },
            {
                'subtitle': 'Key Characteristics',
                'bullets': [
                    '<b>Automated Release Process:</b> Every change is automatically prepared for release',
                    '<b>Manual Approval Gates:</b> Human oversight before production deployment',
                    '<b>Reduced Risk:</b> Smaller, incremental updates minimize deployment risks',
                    '<b>Faster Time to Market:</b> Streamlined processes accelerate delivery',
                    '<b>Consistent Deployments:</b> Automated workflows ensure repeatability'
                ]
            },
            {
                'subtitle': 'AWS CodePipeline for CD',
                'text': 'AWS CodePipeline is a fully managed CI/CD service that automates the software release workflow. It connects source control, building, testing, and deployment stages into a seamless pipeline.'
            },
            {
                'subtitle': 'Pipeline Components',
                'bullets': [
                    '<b>Source Stage:</b> Monitors repositories (CodeCommit, GitHub) for changes',
                    '<b>Build Stage:</b> Compiles and tests code using AWS CodeBuild',
                    '<b>Test Stage:</b> Runs automated tests to validate functionality',
                    '<b>Deploy Stage:</b> Deploys to EC2, ECS, Lambda, or S3',
                    '<b>Manual Approval:</b> Optional checkpoints for review and control'
                ]
            },
            {
                'box': '<b>Event-Driven Execution:</b> CodePipeline automatically triggers new executions whenever changes are pushed to the source repository, ensuring the latest code is always validated and deployed consistently.'
            }
        ]
    )
    
    # 3. AWS CloudFormation
    generator.create_pdf(
        "03_AWS_CloudFormation.pdf",
        "What is AWS CloudFormation?",
        [
            {
                'subtitle': 'Overview',
                'text': 'AWS CloudFormation is a powerful Infrastructure as Code (IaC) service that enables users to model, provision, and manage AWS resources using declarative templates. It eliminates manual configuration by allowing you to define your entire cloud infrastructure in code.'
            },
            {
                'subtitle': 'Core Concepts',
                'bullets': [
                    '<b>Templates:</b> JSON or YAML files that define AWS resources and configurations',
                    '<b>Stacks:</b> Collections of AWS resources managed as a single unit',
                    '<b>Change Sets:</b> Preview proposed infrastructure changes before applying',
                    '<b>Drift Detection:</b> Identify when actual configuration deviates from template',
                    '<b>StackSets:</b> Deploy resources across multiple accounts and regions'
                ]
            },
            {
                'subtitle': 'Key Features',
                'bullets': [
                    'Declarative templates in JSON or YAML format',
                    'Automated resource provisioning and configuration',
                    'Automatic dependency management and ordering',
                    'Automatic rollbacks on errors',
                    'Version control integration for infrastructure changes',
                    'Cross-account and cross-region management',
                    'Integration with AWS CloudFormation Registry for third-party resources'
                ]
            },
            {
                'subtitle': 'Benefits',
                'bullets': [
                    '<b>Automation:</b> Eliminates manual infrastructure setup',
                    '<b>Consistency:</b> Identical deployments across environments',
                    '<b>Repeatability:</b> Rapid and reliable infrastructure replication',
                    '<b>Version Control:</b> Track infrastructure changes over time',
                    '<b>Cost Optimization:</b> Efficient resource provisioning',
                    '<b>Scalability:</b> Easy scaling to meet changing demands'
                ]
            },
            {
                'box': '<b>How It Works:</b> Define your infrastructure in a CloudFormation template → Deploy the template to create a stack → CloudFormation provisions all specified resources in the correct order → Manage the entire infrastructure as a single unit.'
            }
        ]
    )
    
    # 4. CloudFront Origin Failover
    generator.create_pdf(
        "04_CloudFront_Origin_Failover.pdf",
        "Optimizing High Availability with CloudFront Origin Failover",
        [
            {
                'subtitle': 'Overview',
                'text': 'AWS CloudFront origin failover is a critical feature for ensuring high availability of web applications. It automatically switches to a secondary origin when the primary origin becomes unavailable, ensuring continuous content delivery to users.'
            },
            {
                'subtitle': 'How Origin Failover Works',
                'bullets': [
                    '<b>Origin Groups:</b> Configure at least two origins (primary and secondary)',
                    '<b>Failover Criteria:</b> Define HTTP status codes that trigger failover',
                    '<b>Automatic Switching:</b> CloudFront routes to secondary on primary failure',
                    '<b>Primary Preference:</b> Always attempts primary origin first',
                    '<b>Supported Methods:</b> Works with GET, HEAD, and OPTIONS requests'
                ]
            },
            {
                'subtitle': 'Configuration Steps',
                'bullets': [
                    'Ensure your CloudFront distribution has at least two origins',
                    'Navigate to CloudFront console and select your distribution',
                    'Create an origin group with primary and secondary origins',
                    'Specify HTTP status codes for failover (400, 403, 404, 500, 502, 503, 504)',
                    'Update cache behavior to use the origin group',
                    'Test failover by simulating primary origin failure'
                ]
            },
            {
                'subtitle': 'Common Use Cases',
                'bullets': [
                    '<b>S3 Multi-Region:</b> S3 buckets in different regions for disaster recovery',
                    '<b>EC2 Redundancy:</b> Multiple EC2 instances across availability zones',
                    '<b>Hybrid Failover:</b> Combine with Lambda@Edge for advanced logic',
                    '<b>Custom Error Pages:</b> Consistent user experience during failover'
                ]
            },
            {
                'box': '<b>High Availability:</b> Origin failover significantly enhances application reliability by ensuring content delivery even when primary origins fail. Combined with other AWS services, it provides comprehensive disaster recovery solutions.'
            }
        ]
    )
    
    # 5. Lambda@Edge
    generator.create_pdf(
        "05_Lambda_CloudFront_Edge.pdf",
        "Using AWS Lambda with CloudFront Lambda@Edge",
        [
            {
                'subtitle': 'Overview',
                'text': 'Lambda@Edge is a feature of Amazon CloudFront that allows you to run AWS Lambda functions at AWS edge locations globally. This brings computation closer to users, reducing latency and enabling powerful serverless edge computing solutions.'
            },
            {
                'subtitle': 'CloudFront Trigger Points',
                'bullets': [
                    '<b>Viewer Request:</b> Executes when CloudFront receives a request from a viewer',
                    '<b>Origin Request:</b> Executes before CloudFront forwards request to origin',
                    '<b>Origin Response:</b> Executes when CloudFront receives response from origin',
                    '<b>Viewer Response:</b> Executes before CloudFront returns response to viewer'
                ]
            },
            {
                'subtitle': 'Common Use Cases',
                'bullets': [
                    '<b>Content Personalization:</b> Tailor content based on location, device, or user preferences',
                    '<b>A/B Testing:</b> Route users to different versions based on cookies',
                    '<b>Authentication:</b> Validate tokens and enforce access controls',
                    '<b>URL Rewriting:</b> Manipulate URLs and create user-friendly paths',
                    '<b>Security Headers:</b> Add HSTS and other security headers',
                    '<b>Image Optimization:</b> Compress and resize images on-the-fly',
                    '<b>Bot Mitigation:</b> Detect and block malicious traffic at the edge',
                    '<b>Custom Load Balancing:</b> Dynamic origin selection based on conditions'
                ]
            },
            {
                'subtitle': 'Lambda@Edge vs CloudFront Functions',
                'bullets': [
                    '<b>CloudFront Functions:</b> Lightweight, ultra-low latency, simple tasks (header manipulation, basic auth)',
                    '<b>Lambda@Edge:</b> More powerful, complex logic, external API calls, database queries, full request/response body access'
                ]
            },
            {
                'box': '<b>Edge Computing Power:</b> Lambda@Edge enables you to execute custom logic at AWS edge locations worldwide, providing millisecond latency improvements and enhanced user experiences without managing servers.'
            }
        ]
    )
    
    # 6. CodePipeline Best Practices
    generator.create_pdf(
        "06_CodePipeline_Best_Practices.pdf",
        "CodePipeline Best Practices and Use Cases",
        [
            {
                'subtitle': 'Overview',
                'text': 'AWS CodePipeline is a fully managed CI/CD service that automates release pipelines. Following best practices ensures optimal cost, performance, security, and reliability in your deployment workflows.'
            },
            {
                'subtitle': 'Cost Optimization',
                'bullets': [
                    'Delete unused pipelines and stages to minimize costs',
                    'Optimize compute resources with caching and efficient deployments',
                    'Use spot instances for non-production environments',
                    'Implement S3 lifecycle policies for artifact cleanup',
                    'Store only necessary deployment artifacts'
                ]
            },
            {
                'subtitle': 'Performance Optimization',
                'bullets': [
                    '<b>Parallelization:</b> Execute stages concurrently for faster pipelines',
                    '<b>Caching:</b> Cache dependencies and build artifacts to reduce build times',
                    '<b>Modular Design:</b> Break monoliths into smaller, independent pipelines',
                    '<b>Monitoring:</b> Set up CloudWatch alarms for performance tracking',
                    '<b>Parameters:</b> Use pipeline parameters for environment flexibility'
                ]
            },
            {
                'subtitle': 'Security Best Practices',
                'bullets': [
                    'Follow least privilege principle for IAM roles',
                    'Enable artifact encryption using AWS KMS',
                    'Never hardcode secrets in pipeline configurations',
                    'Use AWS Secrets Manager for sensitive information',
                    'Regularly update CodeBuild images and dependencies',
                    'Integrate security scanning tools (SonarQube, Snyk, OWASP ZAP)'
                ]
            },
            {
                'subtitle': 'Operational Best Practices',
                'bullets': [
                    'Separate pipelines for different environments (dev, staging, prod)',
                    'Include comprehensive automated testing early in pipeline',
                    'Integrate with version control systems (CodeCommit, GitHub)',
                    'Define infrastructure as code using CloudFormation',
                    'Set timeouts for each pipeline stage',
                    'Define clear, logical pipeline stages (Source, Build, Test, Deploy)'
                ]
            },
            {
                'box': '<b>Use Cases:</b> Web applications to Elastic Beanstalk, containerized apps to ECS/EKS, serverless Lambda functions, EC2 deployments, infrastructure as code with CloudFormation, and integration with third-party tools.'
            }
        ]
    )
    
    # 7. Continuous Delivery with CodePipeline (duplicate content merged with #2 and #6)
    generator.create_pdf(
        "07_CD_with_CodePipeline.pdf",
        "Continuous Delivery with CodePipeline",
        [
            {
                'subtitle': 'Overview',
                'text': 'AWS CodePipeline enables continuous delivery by automating the entire software release process. It orchestrates source control, building, testing, and deployment into a seamless, event-driven workflow that ensures code is always ready for production.'
            },
            {
                'subtitle': 'Pipeline Architecture',
                'bullets': [
                    '<b>Stages:</b> Logical divisions like Source, Build, Test, Deploy',
                    '<b>Actions:</b> Tasks within each stage (compile, test, deploy)',
                    '<b>Transitions:</b> Automated or manual gates between stages',
                    '<b>Artifacts:</b> Files passed between stages (stored in S3)',
                    '<b>Approvals:</b> Manual checkpoints for production deployments'
                ]
            },
            {
                'subtitle': 'Integration with AWS Services',
                'bullets': [
                    '<b>AWS CodeCommit:</b> Source control and repository management',
                    '<b>AWS CodeBuild:</b> Compiling, testing, and building applications',
                    '<b>AWS CodeDeploy:</b> Automated deployments to EC2, ECS, Lambda',
                    '<b>AWS CloudFormation:</b> Infrastructure as code deployments',
                    '<b>Amazon S3:</b> Artifact storage and static website hosting',
                    '<b>Amazon CloudWatch:</b> Monitoring, logging, and metrics',
                    '<b>AWS X-Ray:</b> End-to-end tracing and debugging'
                ]
            },
            {
                'subtitle': 'Deployment Strategies',
                'bullets': [
                    '<b>Blue/Green:</b> Zero-downtime deployments with traffic switching',
                    '<b>Rolling:</b> Gradual updates to instance subsets',
                    '<b>Canary:</b> Test with small percentage before full rollout',
                    '<b>All-at-Once:</b> Fastest deployment with potential downtime'
                ]
            },
            {
                'subtitle': 'Benefits',
                'bullets': [
                    'Faster delivery of software updates',
                    'Increased consistency and reliability',
                    'Reduced human errors through automation',
                    'Improved scalability for projects of all sizes',
                    'Enhanced developer productivity',
                    'Quicker bug detection and resolution'
                ]
            },
            {
                'box': '<b>Event-Driven Automation:</b> CodePipeline automatically triggers pipeline executions when changes are detected in source repositories, ensuring continuous validation and deployment of the latest code.'
            }
        ]
    )
    
    # 8. AWS CodeCommit
    generator.create_pdf(
        "08_AWS_CodeCommit.pdf",
        "What is AWS CodeCommit?",
        [
            {
                'subtitle': 'Overview',
                'text': 'AWS CodeCommit is a fully managed source control service that hosts secure and highly scalable private Git repositories. It eliminates the need to operate your own source control system or worry about scaling its infrastructure.'
            },
            {
                'subtitle': 'Key Features',
                'bullets': [
                    '<b>Git Compatibility:</b> Fully compatible with standard Git commands and workflows',
                    '<b>Managed Service:</b> AWS handles infrastructure, scaling, and availability',
                    '<b>Unlimited Repositories:</b> Create as many repositories as needed',
                    '<b>Scalability:</b> Handles large codebases and lengthy revision histories',
                    '<b>High Availability:</b> Built-in redundancy and fault tolerance'
                ]
            },
            {
                'subtitle': 'Collaboration Features',
                'bullets': [
                    '<b>Branching and Merging:</b> Standard Git workflows for parallel development',
                    '<b>Pull Requests:</b> Code review and approval workflows',
                    '<b>Code Reviews:</b> Comment and approve changes before merging',
                    '<b>Notifications:</b> Amazon SNS integration for repository events',
                    '<b>Team Collaboration:</b> Multiple developers working simultaneously'
                ]
            },
            {
                'subtitle': 'Security and Access Control',
                'bullets': [
                    '<b>IAM Integration:</b> Fine-grained access control with AWS IAM',
                    '<b>Encryption:</b> Data encrypted at rest and in transit',
                    '<b>MFA Support:</b> Multi-factor authentication for enhanced security',
                    '<b>CloudTrail Logging:</b> Audit trail of all repository activities',
                    '<b>VPC Endpoints:</b> Private connectivity without internet exposure'
                ]
            },
            {
                'subtitle': 'AWS Integration',
                'bullets': [
                    'Seamless integration with AWS CodePipeline for CI/CD',
                    'Works with AWS CodeBuild for automated builds',
                    'Integrates with AWS CodeDeploy for deployments',
                    'Amazon CloudWatch for monitoring and alerts',
                    'AWS CodeGuru Reviewer for automated code analysis'
                ]
            },
            {
                'box': '<b>Fully Managed Git:</b> CodeCommit provides enterprise-grade source control without the operational overhead of managing your own Git servers, with built-in security, scalability, and AWS service integration.'
            }
        ]
    )
    
    # 9. Elastic Beanstalk
    generator.create_pdf(
        "09_Elastic_Beanstalk.pdf",
        "What is AWS Elastic Beanstalk?",
        [
            {
                'subtitle': 'Overview',
                'text': 'AWS Elastic Beanstalk is a Platform as a Service (PaaS) that simplifies deploying and managing web applications. It automatically handles capacity provisioning, load balancing, auto-scaling, and application health monitoring, allowing developers to focus on writing code.'
            },
            {
                'subtitle': 'Supported Platforms',
                'bullets': [
                    'Java, .NET, PHP, Node.js, Python, Ruby, Go',
                    'Docker containers for custom platforms',
                    'Apache, Nginx, Passenger, and IIS servers',
                    'Multiple versions of each platform'
                ]
            },
            {
                'subtitle': 'Key Features',
                'bullets': [
                    '<b>Simplified Deployment:</b> Upload code and Elastic Beanstalk handles the rest',
                    '<b>Automatic Scaling:</b> Adjusts capacity based on traffic automatically',
                    '<b>Managed Infrastructure:</b> AWS manages EC2, load balancers, and networking',
                    '<b>Health Monitoring:</b> Built-in dashboard for application status',
                    '<b>Multiple Environments:</b> Separate dev, staging, and production environments'
                ]
            },
            {
                'subtitle': 'Deployment Strategies',
                'bullets': [
                    '<b>All at Once:</b> Fastest method, may involve brief downtime',
                    '<b>Rolling:</b> Updates instances in batches, reduces downtime',
                    '<b>Rolling with Additional Batch:</b> Maintains full capacity during updates',
                    '<b>Immutable:</b> Deploys to new instances, safe rollback',
                    '<b>Traffic Splitting (Canary):</b> Gradual traffic shift for testing',
                    '<b>Blue/Green:</b> Separate environment with traffic swap'
                ]
            },
            {
                'subtitle': 'AWS Service Integration',
                'bullets': [
                    'Amazon RDS for managed databases',
                    'Amazon S3 for storage',
                    'Amazon CloudWatch for logging and monitoring',
                    'AWS IAM for access control',
                    'Amazon VPC for network isolation',
                    'Elastic Load Balancing for traffic distribution'
                ]
            },
            {
                'box': '<b>PaaS Benefits:</b> Elastic Beanstalk abstracts infrastructure complexity while maintaining full control over AWS resources. You retain the ability to customize configurations while benefiting from automated management.'
            }
        ]
    )
    
    # 10. Amazon API Gateway
    generator.create_pdf(
        "10_Amazon_API_Gateway.pdf",
        "What is Amazon API Gateway?",
        [
            {
                'subtitle': 'Overview',
                'text': 'Amazon API Gateway is a fully managed service for creating, publishing, maintaining, monitoring, and securing REST APIs and WebSocket APIs at any scale. It acts as the "front door" for applications to access data, business logic, or functionality from backend services.'
            },
            {
                'subtitle': 'API Types',
                'bullets': [
                    '<b>REST APIs:</b> Full-featured APIs with caching, throttling, and authorization',
                    '<b>HTTP APIs:</b> Lower-cost, lower-latency option for simple use cases',
                    '<b>WebSocket APIs:</b> Real-time two-way communication'
                ]
            },
            {
                'subtitle': 'Key Features',
                'bullets': [
                    '<b>Traffic Management:</b> Handle hundreds of thousands of concurrent calls',
                    '<b>Request Throttling:</b> Control requests per second for each method',
                    '<b>Caching:</b> Improve performance with response caching',
                    '<b>API Versioning:</b> Run multiple versions simultaneously',
                    '<b>Stage Management:</b> Separate alpha, beta, and production stages',
                    '<b>Custom Domain Names:</b> User-friendly API URLs'
                ]
            },
            {
                'subtitle': 'Security Features',
                'bullets': [
                    '<b>IAM Roles:</b> AWS Identity and Access Management integration',
                    '<b>Custom Authorizers:</b> Lambda-based authorization logic',
                    '<b>Amazon Cognito:</b> User pool integration for authentication',
                    '<b>API Keys:</b> Fine-grained access control for third-party developers',
                    '<b>AWS WAF:</b> Protection against common web exploits',
                    '<b>Mutual TLS:</b> Enhanced security with client certificates',
                    '<b>Private Endpoints:</b> VPC-only access for internal APIs'
                ]
            },
            {
                'subtitle': 'Monitoring and Analytics',
                'bullets': [
                    'Amazon CloudWatch integration for metrics and logs',
                    'API Gateway dashboard for visual monitoring',
                    'AWS X-Ray for end-to-end request tracing',
                    'Detailed metrics on calls, latency, and error rates',
                    'Custom CloudWatch alarms for proactive monitoring'
                ]
            },
            {
                'subtitle': 'Backend Integration',
                'bullets': [
                    'AWS Lambda functions for serverless backends',
                    'HTTP endpoints for existing web services',
                    'AWS services (DynamoDB, S3, SNS, SQS)',
                    'VPC Link for private resources',
                    'Mock integrations for testing'
                ]
            },
            {
                'box': '<b>Best Practices:</b> Implement least privilege IAM policies, enable CloudWatch logs, use latest TLS protocol, enable response caching and encryption, control access with API keys, rotate SSL certificates regularly, and enable X-Ray tracing.'
            }
        ]
    )
    
    # 11. AWS Systems Manager
    generator.create_pdf(
        "11_AWS_Systems_Manager.pdf",
        "What is AWS Systems Manager?",
        [
            {
                'subtitle': 'Overview',
                'text': 'AWS Systems Manager is a comprehensive management service that provides a unified interface to view operational data and automate operational tasks across AWS, on-premises, and hybrid cloud environments. It centralizes infrastructure management at scale.'
            },
            {
                'subtitle': 'Core Capabilities',
                'bullets': [
                    '<b>Automation:</b> Create and execute workflows for common IT operations',
                    '<b>Run Command:</b> Remotely execute commands on instances at scale',
                    '<b>Session Manager:</b> Secure shell access without SSH or bastion hosts',
                    '<b>Patch Manager:</b> Automate OS and application patching',
                    '<b>State Manager:</b> Maintain consistent instance configurations',
                    '<b>Parameter Store:</b> Secure storage for configuration data and secrets',
                    '<b>Inventory:</b> Collect metadata from managed instances',
                    '<b>Maintenance Windows:</b> Schedule operational tasks'
                ]
            },
            {
                'subtitle': 'Automation Features',
                'bullets': [
                    'Automate software patching and updates',
                    'Schedule or trigger workflows by events',
                    'Reduce human error with consistent automation',
                    'Application deployment automation',
                    'Instance provisioning and configuration',
                    'Disaster recovery procedures'
                ]
            },
            {
                'subtitle': 'Security and Compliance',
                'bullets': [
                    '<b>Session Manager:</b> No inbound ports, SSH keys, or bastion hosts needed',
                    '<b>Audit Logging:</b> CloudTrail integration for all activities',
                    '<b>Least Privilege:</b> IAM-based access control',
                    '<b>Encryption:</b> Parameter Store supports KMS encryption',
                    '<b>Compliance Scanning:</b> Check instances against policies',
                    '<b>Configuration Drift:</b> Detect and prevent unauthorized changes'
                ]
            },
            {
                'subtitle': 'Patch Management',
                'bullets': [
                    'Scan instances for missing patches automatically',
                    'Apply security updates to Windows and Linux',
                    'Patch baselines for auto-approving categories',
                    'Maintenance windows for scheduled patching',
                    'Compliance reporting for patch status'
                ]
            },
            {
                'subtitle': 'Hybrid Environment Support',
                'bullets': [
                    'Manage AWS EC2 instances',
                    'Manage on-premises servers',
                    'Manage virtual machines in other clouds',
                    'Unified management interface for all resources',
                    'SSM Agent runs on all managed nodes'
                ]
            },
            {
                'box': '<b>Operational Excellence:</b> Systems Manager simplifies day-to-day operations by enabling organizations to define system configurations, prevent drift, maintain software compliance, and keep infrastructure secure at scale.'
            }
        ]
    )
    
    # 12. Amazon ECS
    generator.create_pdf(
        "12_Amazon_ECS.pdf",
        "What is Amazon Elastic Container Service?",
        [
            {
                'subtitle': 'Overview',
                'text': 'Amazon Elastic Container Service (ECS) is a fully managed container orchestration service that simplifies deploying, managing, and scaling containerized applications using Docker. It provides a highly scalable and performant platform for running containers in the cloud.'
            },
            {
                'subtitle': 'Core Components',
                'bullets': [
                    '<b>Clusters:</b> Logical grouping of resources for containerized applications',
                    '<b>Task Definitions:</b> JSON blueprints specifying container configurations',
                    '<b>Tasks:</b> Running instances of task definitions',
                    '<b>Services:</b> Maintain specified number of tasks with load balancing',
                    '<b>Container Instances:</b> EC2 instances running the ECS agent'
                ]
            },
            {
                'subtitle': 'Launch Types',
                'bullets': [
                    '<b>EC2 Launch Type:</b> Full control over EC2 instances hosting containers, custom configurations, specific instance types',
                    '<b>AWS Fargate:</b> Serverless compute for containers, no server management, pay only for resources used, automatic scaling',
                    '<b>ECS Anywhere:</b> Extend ECS to on-premises servers for hybrid deployments'
                ]
            },
            {
                'subtitle': 'Key Benefits',
                'bullets': [
                    '<b>Scalability:</b> Automatic scaling based on demand (task and infrastructure level)',
                    '<b>High Availability:</b> Built-in fault tolerance and automatic task replacement',
                    '<b>Cost-Effectiveness:</b> Pay-as-you-go pricing, optimized resource usage',
                    '<b>Simplified Management:</b> Fully managed service, focus on applications',
                    '<b>Performance:</b> Fast container startup and efficient resource allocation'
                ]
            },
            {
                'subtitle': 'AWS Integration',
                'bullets': [
                    '<b>Amazon ECR:</b> Container image registry',
                    '<b>AWS Fargate:</b> Serverless compute engine',
                    '<b>Elastic Load Balancing:</b> Traffic distribution across tasks',
                    '<b>Amazon CloudWatch:</b> Monitoring and logging',
                    '<b>AWS IAM:</b> Security and access control',
                    '<b>Amazon VPC:</b> Network isolation',
                    '<b>AWS CodePipeline:</b> CI/CD integration'
                ]
            },
            {
                'subtitle': 'Security Features',
                'bullets': [
                    'IAM roles for tasks with fine-grained permissions',
                    'VPC isolation for network security',
                    'Encryption at rest for container images',
                    'AWS Secrets Manager integration',
                    'Security groups and network ACLs',
                    'CloudTrail logging for audit trails'
                ]
            },
            {
                'box': '<b>Container Orchestration:</b> ECS provides enterprise-grade container orchestration with the flexibility to choose between EC2 for full control or Fargate for serverless simplicity, all while maintaining deep AWS integration.'
            }
        ]
    )
    
    # 13. AWS X-Ray
    generator.create_pdf(
        "13_AWS_X-Ray.pdf",
        "What is AWS X-Ray?",
        [
            {
                'subtitle': 'Overview',
                'text': 'AWS X-Ray is a distributed tracing service that provides comprehensive insights into application performance and behavior. It helps developers debug, analyze, and optimize distributed applications, especially microservices architectures running on AWS.'
            },
            {
                'subtitle': 'Core Concepts',
                'bullets': [
                    '<b>Traces:</b> Complete journey of a single request through your application',
                    '<b>Segments:</b> Data recorded from individual services handling the request',
                    '<b>Subsegments:</b> Finer granularity within services (database queries, API calls)',
                    '<b>Annotations:</b> Custom metadata for filtering and analysis',
                    '<b>Service Map:</b> Visual representation of application architecture'
                ]
            },
            {
                'subtitle': 'Key Features',
                'bullets': [
                    '<b>End-to-End Tracing:</b> Track requests across all application components',
                    '<b>Service Map:</b> Automatically generated visual architecture diagram',
                    '<b>Performance Analysis:</b> Identify bottlenecks and latency issues',
                    '<b>Error Detection:</b> Automatic flagging of errors and faults',
                    '<b>Root Cause Analysis:</b> Detailed trace data with error logs and stack traces',
                    '<b>Latency Distribution:</b> Understand performance patterns',
                    '<b>Custom Annotations:</b> Add metadata for precise filtering'
                ]
            },
            {
                'subtitle': 'Debugging Capabilities',
                'bullets': [
                    'Visual service map highlights problematic areas',
                    'Pinpoint performance bottlenecks across services',
                    'Identify elevated error rates quickly',
                    'Detailed trace-level data for investigation',
                    'Real-time visualization reduces troubleshooting time',
                    'Automated error and fault detection',
                    'X-Ray Analytics for in-depth analysis'
                ]
            },
            {
                'subtitle': 'AWS Integration',
                'bullets': [
                    'Amazon EC2, ECS, EKS for compute',
                    'AWS Lambda for serverless functions',
                    'Amazon API Gateway for REST APIs',
                    'Amazon SNS, SQS for messaging',
                    'Amazon EventBridge for event-driven architectures',
                    'Elastic Load Balancing for distributed traffic'
                ]
            },
            {
                'subtitle': 'Implementation',
                'bullets': [
                    'Instrument applications using X-Ray SDKs',
                    'SDKs available for multiple programming languages',
                    'X-Ray daemon collects and forwards trace data',
                    'Minimal code changes required',
                    'Automatic instrumentation for many AWS services',
                    'Custom instrumentation for detailed insights'
                ]
            },
            {
                'box': '<b>Distributed Tracing:</b> X-Ray provides complete visibility into distributed applications, enabling faster debugging, performance optimization, and improved reliability through comprehensive request tracking and analysis.'
            }
        ]
    )
    
    # 14. AppSpec Hooks for ECS
    generator.create_pdf(
        "14_AppSpec_Hooks_ECS.pdf",
        "AppSpec 'hooks' Section for Amazon ECS Deployment",
        [
            {
                'subtitle': 'Overview',
                'text': 'AWS CodeDeploy uses AppSpec files to manage ECS deployments. The hooks section enables integration of custom logic via AWS Lambda functions at various stages of the deployment lifecycle, allowing for validation, testing, and custom actions.'
            },
            {
                'subtitle': 'AppSpec File Structure',
                'text': 'For ECS deployments, the AppSpec file is in YAML or JSON format and specifies the ECS task definition, load balancer information, and optional Lambda functions for lifecycle hooks.'
            },
            {
                'subtitle': 'ECS Deployment Lifecycle Hooks',
                'bullets': [
                    '<b>BeforeInstall:</b> Run tasks before replacement task set is created',
                    '<b>AfterInstall:</b> Run tasks after replacement task set is created',
                    '<b>AfterAllowTestTraffic:</b> Run tests after test traffic is routed',
                    '<b>BeforeAllowTraffic:</b> Run tasks before production traffic shift',
                    '<b>AfterAllowTraffic:</b> Run tasks after production traffic shift'
                ]
            },
            {
                'subtitle': 'Hook Configuration',
                'bullets': [
                    'Each hook specifies a Lambda function ARN',
                    'Lambda functions receive deployment lifecycle event data',
                    'Functions must call CodeDeploy to continue or fail deployment',
                    'Timeout can be configured for each hook (default 1 hour)',
                    'Hooks enable automated validation and testing'
                ]
            },
            {
                'subtitle': 'Common Use Cases',
                'bullets': [
                    '<b>Health Checks:</b> Verify new task set is healthy before traffic shift',
                    '<b>Integration Tests:</b> Run automated tests against new version',
                    '<b>Smoke Tests:</b> Basic functionality validation',
                    '<b>Monitoring Setup:</b> Configure CloudWatch alarms for new tasks',
                    '<b>Notifications:</b> Send alerts about deployment progress',
                    '<b>Rollback Logic:</b> Custom conditions for automatic rollback'
                ]
            },
            {
                'subtitle': 'Best Practices',
                'bullets': [
                    'Keep Lambda functions lightweight and focused',
                    'Implement proper error handling in hook functions',
                    'Set appropriate timeouts for each hook',
                    'Log detailed information for troubleshooting',
                    'Test hooks thoroughly in non-production environments',
                    'Use IAM roles with least privilege for Lambda functions'
                ]
            },
            {
                'box': '<b>Deployment Validation:</b> AppSpec hooks for ECS enable automated validation and testing at critical points in the deployment lifecycle, ensuring safe and reliable container deployments with custom logic.'
            }
        ]
    )
    
    # 15. CodeDeploy Deployments
    generator.create_pdf(
        "15_CodeDeploy_Deployments.pdf",
        "AWS CodeDeploy Deployment Strategies",
        [
            {
                'subtitle': 'Overview',
                'text': 'AWS CodeDeploy automates application deployments to various compute platforms including EC2, Lambda, and ECS. It offers multiple deployment strategies to minimize downtime, manage risk, and ensure reliable software releases.'
            },
            {
                'subtitle': 'Supported Platforms',
                'bullets': [
                    'Amazon EC2 instances',
                    'On-premises servers',
                    'AWS Lambda functions',
                    'Amazon ECS services'
                ]
            },
            {
                'subtitle': 'In-Place Deployment',
                'bullets': [
                    'Application stopped on each instance in deployment group',
                    'Latest revision installed on same instances',
                    'New version started and validated',
                    'Load balancer can deregister instances during deployment',
                    'Only available for EC2/On-Premises platform',
                    'Cost-effective but may have brief downtime'
                ]
            },
            {
                'subtitle': 'Blue/Green Deployment',
                'bullets': [
                    'Provision entirely new set of servers (green environment)',
                    'Current blue environment remains active during deployment',
                    'Traffic switched from blue to green after validation',
                    'Old blue environment decommissioned after successful deployment',
                    'Minimizes downtime and simplifies rollback',
                    'Only deployment type for Lambda and ECS',
                    'Also supported for EC2/On-Premises',
                    'Requires additional infrastructure during transition'
                ]
            },
            {
                'subtitle': 'Rolling Deployment',
                'bullets': [
                    'Gradually replaces instances with new version',
                    'Deploys to subset of instances at a time',
                    'Reduces downtime compared to in-place',
                    'Slower rollout process',
                    'Maintains partial availability during deployment'
                ]
            },
            {
                'subtitle': 'Canary Deployment',
                'bullets': [
                    'Specialized form of blue/green deployment',
                    'New version rolled out to small percentage of users first',
                    'Early detection of issues with minimal impact',
                    'Gradually shift more traffic to new version',
                    'Controlled and gradual rollout',
                    'Applicable to Lambda and ECS'
                ]
            },
            {
                'subtitle': 'Deployment Configurations',
                'bullets': [
                    '<b>AllAtOnce:</b> Deploy to all instances simultaneously',
                    '<b>HalfAtATime:</b> Deploy to 50% of instances at once',
                    '<b>OneAtATime:</b> Deploy to one instance at a time',
                    '<b>Custom:</b> Define your own deployment configuration'
                ]
            },
            {
                'box': '<b>Strategy Selection:</b> Choose deployment strategy based on acceptable downtime, rollback requirements, and risk tolerance. Blue/green offers safest rollback, canary enables gradual testing, and in-place is most cost-effective.'
            }
        ]
    )
    
    # 16. AppSpec Hooks for EC2/On-Premises
    generator.create_pdf(
        "16_AppSpec_Hooks_EC2.pdf",
        "AppSpec 'hooks' Section for EC2/On-Premises Deployment",
        [
            {
                'subtitle': 'Overview',
                'text': 'AWS CodeDeploy uses the AppSpec file (appspec.yml) to manage deployments to EC2 instances and on-premises servers. The hooks section maps deployment lifecycle events to scripts, enabling automation of tasks at different deployment stages.'
            },
            {
                'subtitle': 'AppSpec File Structure',
                'bullets': [
                    '<b>version:</b> AppSpec format version (currently 0.0)',
                    '<b>os:</b> Operating system (linux or windows)',
                    '<b>files:</b> Source and destination for application files',
                    '<b>hooks:</b> Lifecycle events mapped to scripts'
                ]
            },
            {
                'subtitle': 'Lifecycle Event Hooks (Execution Order)',
                'bullets': [
                    '<b>BeforeBlockTraffic:</b> Tasks before load balancer deregistration',
                    '<b>BlockTraffic:</b> Deregister instances from load balancer',
                    '<b>AfterBlockTraffic:</b> Tasks after deregistration',
                    '<b>ApplicationStop:</b> Gracefully stop current application',
                    '<b>DownloadBundle:</b> Agent copies revision files (reserved)',
                    '<b>BeforeInstall:</b> Pre-installation tasks (backup, decrypt, install dependencies)',
                    '<b>Install:</b> Agent copies files to final destination (reserved)',
                    '<b>AfterInstall:</b> Post-installation configuration changes',
                    '<b>ApplicationStart:</b> Start newly deployed application',
                    '<b>ValidateService:</b> Post-deployment validation tests',
                    '<b>BeforeAllowTraffic:</b> Tasks before load balancer registration',
                    '<b>AllowTraffic:</b> Register instances with load balancer',
                    '<b>AfterAllowTraffic:</b> Final validation and smoke tests'
                ]
            },
            {
                'subtitle': 'Hook Script Capabilities',
                'bullets': [
                    'Unzip application files',
                    'Run functional tests',
                    'Manage load balancer registration',
                    'Configure application settings',
                    'Backup current version',
                    'Install dependencies',
                    'Decrypt sensitive files',
                    'Validate deployment success'
                ]
            },
            {
                'subtitle': 'Important Notes',
                'bullets': [
                    'Hooks execute once per deployment to an instance',
                    'AppSpec file must be in root of application source',
                    'EC2/On-Premises uses YAML format only',
                    'DownloadBundle and Install are reserved for CodeDeploy agent',
                    'Scripts can be shell scripts, PowerShell, or executables',
                    'Timeout can be configured for each hook'
                ]
            },
            {
                'box': '<b>Deployment Automation:</b> AppSpec hooks enable comprehensive automation of deployment tasks, from graceful application shutdown to validation testing, ensuring reliable and consistent deployments to EC2 and on-premises infrastructure.'
            }
        ]
    )
    
    print("\n" + "="*60)
    print("✓ All 16 AWS PDF files created successfully!")
    print(f"✓ Location: {os.path.abspath(generator.output_dir)}")
    print("="*60)

if __name__ == "__main__":
    main()
