# API examples

## Health
```powershell
curl http://127.0.0.1:8000/health
```

## Weather
```powershell
curl http://127.0.0.1:8000/weather
```

## Products
```powershell
curl http://127.0.0.1:8000/products
```

## Product
```powershell
curl http://127.0.0.1:8000/products/GROC-001
```

## AI question
```powershell
curl -X POST http://127.0.0.1:8000/ask `
  -H "Content-Type: application/json" `
  -d '{"question":"Is GROC-001 within its documented limits under the current weather?"}'
```
