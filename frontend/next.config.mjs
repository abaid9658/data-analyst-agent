/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Configure rewrites to proxy API requests to backend
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: "http://backend:8000/api/v1/:path*",
      },
    ];
  },
};

export default nextConfig;
