const nextJest = require('next/jest');
const createJestConfig = nextJest({ dir: './' });
module.exports = createJestConfig({ testEnvironment: 'jest-environment-jsdom', setupFilesAfterEnv: ['<rootDir>/__tests__/setup.ts'], testPathIgnorePatterns: ['/node_modules/', '/.next/', '/__tests__/setup.ts$'] });
