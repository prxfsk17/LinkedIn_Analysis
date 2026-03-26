"""Data extraction functions for job details."""

import re
from typing import Dict, Optional, Tuple, Set, List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def extract_work_details(content: WebElement) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract work format and employment type from job details.

    Args:
        content: WebElement containing job details

    Returns:
        Tuple of (work_format, employment_type)
        work_format: 'remote', 'hybrid', 'on-site', or None
        employment_type: 'full-time', 'part-time', 'contract', 'internship', or None
    """
    work_format: Optional[str] = None
    employment_type: Optional[str] = None

    try:
        elements: List[WebElement] = content.find_elements(By.CSS_SELECTOR, 'button span span strong')

        for el in elements:
            text: str = el.text.strip().lower()

            if any(x in text for x in ['junior', 'senior', 'mid', 'skill']):
                continue

            # Work format detection
            if 'remote' in text or 'удален' in text:
                work_format = 'remote'
            elif 'hybrid' in text or 'гибрид' in text:
                work_format = 'hybrid'
            elif 'office' in text or 'офис' in text or 'on-site' in text:
                work_format = 'on-site'

            # Employment type detection
            if 'full-time' in text or 'full time' in text or 'полный рабочий день' in text:
                employment_type = 'full-time'
            elif 'part-time' in text or 'part time' in text or 'частичная занятость' in text:
                employment_type = 'part-time'
            elif 'contract' in text or 'b2b' in text or 'договор' in text:
                employment_type = 'contract'
            elif 'internship' in text or 'trainee' in text or 'стажер' in text:
                employment_type = 'internship'

    except Exception:
        pass

    return work_format, employment_type


def extract_seniority_from_text(text: Optional[str]) -> Optional[str]:
    """
    Extract seniority level from text using keyword matching.

    Args:
        text: Text to analyze (title or description)

    Returns:
        Seniority level string or None
    """
    if not text:
        return None

    text_lower: str = text.lower()

    levels: Dict[str, Dict[str, object]] = {
        'director': {
            'keywords': ['director', 'head of', 'vp', 'vice president', 'cto', 'chief'],
            'priority': 100
        },
        'staff': {
            'keywords': ['staff engineer', 'principal engineer', 'distinguished'],
            'priority': 90
        },
        'lead': {
            'keywords': ['team lead', 'tech lead', 'lead engineer', 'lead developer'],
            'priority': 80
        },
        'senior': {
            'keywords': ['senior', 'sr.', 'sr'],
            'priority': 70
        },
        'mid': {
            'keywords': ['mid', 'middle', 'mid-level', 'intermediate'],
            'priority': 50
        },
        'junior': {
            'keywords': ['junior', 'jr.', 'jr'],
            'priority': 30
        },
        'entry': {
            'keywords': ['entry level', 'graduate'],
            'priority': 20
        },
        'internship': {
            'keywords': ['internship', 'trainee', 'intern'],
            'priority': 10
        }
    }

    found_levels: List[Tuple[str, int]] = []

    for level, data in levels.items():
        keywords: List[str] = data['keywords']
        priority: int = data['priority']

        for keyword in keywords:
            pattern: str = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_lower):
                found_levels.append((level, priority))
                break

    if found_levels:
        found_levels.sort(key=lambda x: x[1], reverse=True)
        return found_levels[0][0]

    return None


def extract_tech_skills(text: str) -> Dict[str, bool]:
    """
    Extract technical skills from text and return dict with True/False for each skill.

    Args:
        text: Description text to analyze

    Returns:
        Dictionary with skill names as keys and boolean presence indicator
    """
    text_lower: str = text.lower()

    tech_stack: Dict[str, List[str]] = {
        'python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'scikit-learn', 'pytorch', 'tensorflow',
                   'keras', 'jupyter', 'conda'],
        'java': ['java', 'spring', 'spring boot', 'hibernate', 'maven', 'gradle', 'jpa', 'j2ee', 'jakarta ee'],
        'javascript': ['javascript', 'js', 'ecmascript', 'es6'],
        'typescript': ['typescript', 'ts'],
        'csharp': ['c#', 'csharp', '.net', 'dotnet', 'asp.net', 'entity framework', 'linq', 'xamarin'],
        'cpp': ['c++', 'cpp', 'c plus plus', 'unreal engine', 'ue4', 'ue5', 'qt'],
        'go': ['go', 'golang'],
        'rust': ['rust', 'cargo'],
        'ruby': ['ruby', 'ruby on rails', 'rails'],
        'php': ['php', 'laravel', 'symfony', 'wordpress', 'drupal', 'yii'],
        'swift': ['swift', 'swiftui', 'ios', 'cocoa touch'],
        'kotlin': ['kotlin', 'android', 'jetpack'],
        'r': ['r', 'r language', 'r programming'],
        'scala': ['scala', 'akka', 'spark'],
        'perl': ['perl'],
        'lua': ['lua'],
        'react': ['react', 'react.js', 'reactjs', 'next.js', 'nextjs', 'redux'],
        'angular': ['angular', 'angular.js', 'angularjs', 'ngx'],
        'vue': ['vue', 'vue.js', 'vuejs', 'nuxt', 'nuxt.js'],
        'html_css': ['html', 'css', 'html5', 'css3', 'sass', 'scss', 'less', 'tailwind', 'bootstrap', 'flexbox',
                     'grid'],
        'nodejs': ['node.js', 'nodejs', 'express', 'express.js', 'nest.js', 'nestjs'],
        'graphql': ['graphql', 'apollo', 'relay'],
        'rest': ['rest', 'restful', 'rest api', 'restful api'],
        'postgresql': ['postgresql', 'postgres', 'pl/pgsql'],
        'mysql': ['mysql', 'mariadb'],
        'oracle': ['oracle', 'pl/sql'],
        'mssql': ['sql server', 'mssql', 'microsoft sql', 't-sql', 'tsql'],
        'sqlite': ['sqlite'],
        'mongodb': ['mongodb', 'mongo'],
        'redis': ['redis'],
        'cassandra': ['cassandra', 'astra'],
        'elasticsearch': ['elasticsearch', 'elastic', 'elk'],
        'dynamodb': ['dynamodb', 'dynamo'],
        'couchbase': ['couchbase'],
        'neo4j': ['neo4j', 'graph database'],
        'spark': ['spark', 'apache spark', 'pyspark', 'spark sql'],
        'hadoop': ['hadoop', 'hdfs', 'hive', 'hbase'],
        'kafka': ['kafka', 'apache kafka', 'confluent'],
        'flink': ['flink', 'apache flink'],
        'airflow': ['airflow', 'apache airflow'],
        'databricks': ['databricks'],
        'snowflake': ['snowflake'],
        'bigquery': ['bigquery', 'google bigquery'],
        'redshift': ['redshift', 'amazon redshift'],
        'aws': ['aws', 'amazon web services', 'ec2', 's3', 'lambda', 'rds', 'cloudfront', 'route53', 'eks', 'ecs',
                'cloudformation', 'amplify', 'api gateway', 'step functions'],
        'azure': ['azure', 'microsoft azure', 'aks', 'azure devops', 'app service', 'azure functions', 'cosmos db',
                  'adf'],
        'gcp': ['gcp', 'google cloud', 'google cloud platform', 'gke', 'compute engine', 'cloud run', 'cloud functions',
                'app engine', 'dataflow', 'dataproc'],
        'docker': ['docker', 'dockerfile', 'container', 'containerd'],
        'kubernetes': ['kubernetes', 'k8s', 'k3s', 'openshift', 'eks', 'aks', 'gke'],
        'terraform': ['terraform', 'iac', 'infrastructure as code', 'hcl'],
        'ansible': ['ansible', 'playbook'],
        'jenkins': ['jenkins', 'jenkinsfile'],
        'gitlab_ci': ['gitlab ci', 'gitlab-ci', 'gitlab pipeline'],
        'github_actions': ['github actions', 'github action', 'actions workflow'],
        'circleci': ['circleci', 'circle ci'],
        'teamcity': ['teamcity'],
        'prometheus': ['prometheus', 'monitoring'],
        'grafana': ['grafana', 'observability'],
        'datadog': ['datadog'],
        'splunk': ['splunk'],
        'git': ['git', 'github', 'gitlab', 'bitbucket', 'gitflow'],
        'unit_testing': ['unit test', 'junit', 'pytest', 'unittest', 'xunit', 'testng', 'mocha', 'jest'],
        'integration_testing': ['integration test', 'testcontainers'],
        'e2e_testing': ['e2e', 'end-to-end', 'selenium', 'cypress', 'playwright', 'puppeteer', 'cucumber', 'gherkin'],
        'tdd': ['tdd', 'test driven development'],
        'bdd': ['bdd', 'behavior driven development'],
        'machine_learning': ['machine learning', 'ml', 'deep learning', 'dl', 'ai', 'artificial intelligence', 'llm',
                             'large language model', 'rag', 'langchain', 'openai', 'gpt', 'bert', 'transformers'],
        'data_science': ['data science', 'data scientist', 'statistics', 'statistical analysis', 'predictive modeling',
                         'forecasting'],
        'data_analysis': ['data analysis', 'data analytics', 'analytics', 'business intelligence', 'bi'],
        'data_visualization': ['visualization', 'data visualization', 'tableau', 'power bi', 'looker', 'qlik',
                               'metabase', 'superset'],
        'etl': ['etl', 'elt', 'data pipeline', 'data warehouse', 'data warehousing', 'dwh'],
        'agile': ['agile', 'scrum', 'kanban', 'sprint', 'scrum master', 'product owner', 'backlog', 'jira',
                  'confluence'],
        'team_leadership': ['team lead', 'leadership', 'mentoring', 'tech lead', 'team management'],
        'communication': ['communication skills', 'verbal communication', 'written communication', 'collaboration',
                          'teamwork'],
        'problem_solving': ['problem solving', 'analytical skills', 'critical thinking', 'troubleshooting'],
        'english': ['english', 'fluent english', 'advanced english', 'english proficiency', 'business english',
                    'c1 english', 'b2 english'],
        'polish': ['polish', 'polski', 'język polski', 'native polish', 'polish proficiency', 'polish language',
                   'polska'],
        'german': ['german', 'deutsch', 'german language', 'deutschkenntnisse', 'deutsch sprache'],
        'french': ['french', 'français', 'french language'],
        'spanish': ['spanish', 'español', 'spanish language'],
        'russian': ['russian', 'русский', 'russian language'],
        'ukrainian': ['ukrainian', 'українська', 'ukrainian language'],
        'microservices': ['microservices', 'micro-service', 'microservice architecture', 'distributed systems',
                          'service mesh', 'istio'],
        'event_driven': ['event-driven', 'event driven', 'event sourcing', 'cqrs', 'message broker', 'rabbitmq',
                         'activemq'],
        'security': ['security', 'cybersecurity', 'application security', 'appsec', 'oauth', 'jwt', 'authentication',
                     'authorization', 'encryption', 'owasp'],
        'system_design': ['system design', 'architecture', 'software architecture', 'high-level design', 'hld',
                          'low-level design', 'lld'],
        'monitoring': ['monitoring', 'observability', 'logging', 'alerting', 'opentelemetry'],
        'unity': [' unity ', 'unity3d', ' unity engine', 'c# unity'],
        'unreal': ['unreal', 'unreal engine', 'ue4', 'ue5', 'blueprints', 'c++ unreal'],
        'ios': ['ios', 'iphone', 'ipad', 'swift', 'objective-c', 'cocoa'],
        'android': ['android', 'kotlin', 'java android', 'jetpack compose'],
        'flutter': ['flutter', 'dart', 'flutter framework'],
        'react_native': ['react native', 'rn'],
        'blockchain': ['blockchain', 'ethereum', 'solidity', 'web3', 'crypto', 'smart contracts'],
        'embedded': ['embedded', 'iot', 'internet of things', 'firmware', 'microcontroller', 'arm', 'rtos'],
        'devops': ['devops', 'ci/cd', 'continuous integration', 'continuous delivery', 'continuous deployment']
    }

    result: Dict[str, bool] = {}

    for skill, keywords in tech_stack.items():
        found: bool = False
        for keyword in keywords:
            if len(keyword) <= 3 and keyword.isalpha():
                pattern: str = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    found = True
                    break
            else:
                if keyword in text_lower:
                    found = True
                    break
        result[skill] = found

    return result