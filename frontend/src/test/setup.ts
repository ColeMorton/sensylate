import '@testing-library/jest-dom';

// Mock JSON data for tests
const mockSearchData = [
  {
    group: 'blog',
    slug: 'test-post-1',
    frontmatter: {
      title: 'Test Post 1',
      description: 'This is a test post for search functionality',
      categories: ['technology', 'web'],
      tags: ['astro', 'react'],
      author: 'Test Author',
      date: new Date('2024-01-01')
    },
    content: 'Test content for post 1'
  },
  {
    group: 'blog', 
    slug: 'test-post-2',
    frontmatter: {
      title: 'Another Test Post',
      description: 'Second test post for comprehensive testing',
      categories: ['design'],
      tags: ['ui', 'ux'],
      author: 'Test Author 2',
      date: new Date('2024-01-02')
    },
    content: 'Test content for post 2'
  }
];

// Mock the JSON import that SearchModal depends on
vi.mock('.json/search.json', () => ({
  default: mockSearchData
}));

// Global test utilities
global.mockSearchData = mockSearchData;