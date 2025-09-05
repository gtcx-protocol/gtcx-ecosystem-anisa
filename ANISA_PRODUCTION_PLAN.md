# ANISA Production Readiness Plan

## Current State Assessment

### ✅ What's Already Built
- FastAPI web service with REST endpoints
- Cultural intelligence core engine
- Integration points for PANX/Cortex/GCI
- Basic cultural context detection
- API authentication (API key)
- Demo endpoints

### ❌ What's Missing for Production
1. **Deployment Infrastructure**
   - No Dockerfile
   - No docker-compose configuration
   - No production requirements.txt
   - No database persistence

2. **Production Features**
   - No health/metrics endpoints
   - No rate limiting
   - No request tracing
   - No error handling middleware
   - No database for cultural data

3. **Integration**
   - Not integrated with PANX verification flow
   - Not connected to Cortex analytics
   - No webhook system

## Production Roadmap

### Phase 1: Core Infrastructure (Immediate)
- [ ] Create Dockerfile
- [ ] Add docker-compose integration
- [ ] Create requirements.txt
- [ ] Add health/metrics endpoints
- [ ] Add database models (PostgreSQL)

### Phase 2: Production Features (v1.0)
- [ ] Rate limiting
- [ ] Request ID propagation
- [ ] Structured logging
- [ ] Error handling
- [ ] API versioning
- [ ] OpenAPI documentation

### Phase 3: GTCX Integration (v1.1)
- [ ] PANX integration (cultural consensus weights)
- [ ] Cortex integration (cultural analytics)
- [ ] GCI integration (cultural compliance factors)
- [ ] Event streaming to Cortex

### Phase 4: Advanced Features (v2.0)
- [ ] ML model integration
- [ ] Multi-language support
- [ ] Cultural knowledge graph
- [ ] Community validation system
- [ ] Real-time cultural insights

## Immediate Actions

### 1. Create Production Requirements
```python
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
httpx==0.25.1
prometheus-client==0.19.0
structlog==23.2.0
python-multipart==0.0.6
```

### 2. Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY configs/ ./configs/

ENV PYTHONPATH=/app

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8083"]
```

### 3. Add to Docker Compose
```yaml
# In gtcx-ecosystem-cognitive/infra/compose-prod/docker-compose.yml
anisa:
  build:
    context: ../../../gtcx-ecosystem-anisa
    dockerfile: Dockerfile
  environment:
    - ANISA_PORT=8083
    - ANISA_API_KEY=${ANISA_API_KEY}
    - ANISA_DB_URL=${ANISA_DB_URL:-postgresql://gtcx:gtcx@db:5432/gtcx}
    - PANX_URL=http://panx:8081
    - CORTEX_URL=http://cortex:8082
  depends_on:
    - db
  restart: always
```

### 4. Database Models
```python
# src/models/db.py
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CulturalContext(Base):
    __tablename__ = "cultural_contexts"
    
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    region = Column(String, nullable=False)
    variant = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    cultural_markers = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class CulturalInsight(Base):
    __tablename__ = "cultural_insights"
    
    id = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False)
    cultural_factors = Column(JSON)
    recommendations = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 5. Integration Endpoints
```python
# Add to src/api.py

@app.post("/api/v1/panx/cultural_weight")
async def get_cultural_consensus_weight(
    event_type: str,
    validators: List[str],
    region: str
) -> Dict[str, float]:
    """Provide cultural weights for PANX consensus."""
    # Return role weights based on cultural context
    
@app.post("/api/v1/cortex/cultural_event")
async def send_cultural_event_to_cortex(
    event: Dict[str, Any]
) -> Dict[str, str]:
    """Forward cultural events to Cortex for analytics."""
    # Send to Cortex ingest endpoint
```

## Success Metrics

### Technical Metrics
- [ ] p95 latency < 200ms
- [ ] Availability > 99.9%
- [ ] Error rate < 0.1%
- [ ] Database query time < 50ms

### Business Metrics
- [ ] Cultural context detection accuracy > 85%
- [ ] Integration with 100% of PANX verifications
- [ ] Support for 5+ cultural regions
- [ ] 10+ cultural factors per decision

## Timeline

- **Week 1**: Core infrastructure (Docker, DB, health endpoints)
- **Week 2**: Production features (rate limiting, logging, metrics)
- **Week 3**: PANX/Cortex integration
- **Week 4**: Testing and deployment

## Next Steps

1. Create requirements.txt
2. Build Dockerfile
3. Add database models
4. Integrate with PANX/Cortex
5. Deploy alongside PANX/Cortex
