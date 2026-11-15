/**
 * BibTeX Citation Generator Service
 */

export const bibtexService = {
  formatBibtex(ref) {
    if (!ref) return '';
    const authorFirst = ref.authors 
      ? ref.authors.split(',')[0].trim().replace(/[^a-zA-Z]/g, '') 
      : 'Author';
    const year = ref.year || '2025';
    const key = `${authorFirst}${year}`;

    return `@article{${key},
  title = {${ref.title || 'Sand and Dust Storm Forecasting Research'}},
  author = {${ref.authors || 'Research Author'}},
  journal = {${ref.journal || 'Environmental Science & Atmospheric Technology'}},
  year = {${year}}${ref.volume ? `,\n  volume = {${ref.volume}}` : ''}${ref.pages ? `,\n  pages = {${ref.pages}}` : ''}${ref.doi ? `,\n  doi = {${ref.doi}}` : ''}
}`;
  }
};
