# Vercel Speed Insights Configuration

## Overview

Vercel Speed Insights has been integrated into the Interceptor_M project to monitor real-world performance metrics for web pages. This allows tracking of Core Web Vitals and other performance indicators when the application is deployed on Vercel.

## Implementation Details

### Python Backend Integration

Since this is a Python-based project (Flask + Starlette), Speed Insights is implemented using the vanilla JavaScript approach as documented in the [Vercel Speed Insights Quickstart](https://vercel.com/docs/speed-insights/quickstart).

### Files Modified

#### 1. `app.py` (Flask Application)
- Enhanced the HTML response with proper DOCTYPE and structure
- Added Speed Insights initialization script in the `<head>` section:
  ```javascript
  window.si = window.si || function () { (window.siq = window.siq || []).push(arguments); };
  ```
- Added the Speed Insights script tag:
  ```html
  <script defer src="/_vercel/speed-insights/script.js"></script>
  ```

#### 2. `api/index.py` (Starlette/ASGI Application)
- Added `HTMLResponse` import for serving HTML content
- Created new `/dashboard` endpoint that serves an HTML page with Speed Insights enabled
- Updated the root handler to indicate Speed Insights is enabled
- Applied the same Speed Insights script initialization pattern

### How It Works

1. **Script Initialization**: The inline script creates a global `window.si` function that queues analytics calls
2. **Deferred Loading**: The Speed Insights script loads asynchronously without blocking page rendering
3. **Automatic Collection**: Once loaded, Speed Insights automatically collects Core Web Vitals:
   - **LCP** (Largest Contentful Paint)
   - **FID** (First Input Delay)
   - **CLS** (Cumulative Layout Shift)
   - **TTFB** (Time to First Byte)

### Endpoints with Speed Insights

- **Flask App** (`app.py`):
  - `GET /` - Todos page with Speed Insights enabled

- **Starlette API** (`api/index.py`):
  - `GET /dashboard` - Dashboard page with Speed Insights enabled
  - `GET /` - JSON API (metadata includes speed_insights status)
  - `GET /health` - Health check endpoint

## Enabling Speed Insights on Vercel

### Prerequisites
1. Project must be deployed to Vercel
2. Speed Insights must be enabled in the Vercel dashboard

### Steps to Enable

1. Navigate to your Vercel dashboard
2. Select the Interceptor_M project
3. Go to the "Speed Insights" tab in the sidebar
4. Click the "Enable" button
5. Redeploy your application if needed

### Viewing Analytics

Once enabled and deployed:
1. Visit your deployed application URLs (especially HTML pages)
2. Navigate to the Speed Insights tab in your Vercel dashboard
3. View real-time performance metrics and Core Web Vitals
4. Analyze performance trends over time

## Testing Locally

Speed Insights requires deployment to Vercel to function properly. The script will:
- Load successfully when deployed to Vercel
- Fail gracefully in local development (script won't be available at `/_vercel/speed-insights/script.js`)

To test locally:
```bash
# Run Flask app
python app.py

# Or use Vercel CLI for local testing
vercel dev
```

## Best Practices

1. **Enable on Production**: Speed Insights is most valuable on production deployments
2. **Monitor Regularly**: Check the dashboard weekly to identify performance regressions
3. **Optimize Based on Data**: Use the insights to prioritize performance improvements
4. **Consider Budget**: Speed Insights may have usage limits based on your Vercel plan

## Additional Resources

- [Vercel Speed Insights Documentation](https://vercel.com/docs/speed-insights)
- [Core Web Vitals Overview](https://web.dev/vitals/)
- [Vercel Analytics vs Speed Insights](https://vercel.com/docs/analytics)

## Notes

- Speed Insights is specifically designed for frontend performance monitoring
- No NPM package installation is required for Python projects (uses script tag approach)
- The implementation follows Vercel's recommended pattern for non-JavaScript frameworks
- Speed Insights data is collected from real users visiting your deployed application
