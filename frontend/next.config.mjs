/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Allow external avatar image domains
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "avatars.githubusercontent.com" },
      { protocol: "https", hostname: "lh3.googleusercontent.com" },
      { protocol: "https", hostname: "*.googleusercontent.com" },
    ],
  },

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
