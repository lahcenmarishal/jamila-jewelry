import { describe, expect, it } from 'vitest';
import products from '@/data/imports/jewelry-2026-11.json';

describe('Import bijoux novembre 2026', () => {
  it('respecte les prix compris entre 99 et 199 DH', () => {
    expect(products).toHaveLength(16);
    for (const product of products) {
      expect(product.price).toBeGreaterThanOrEqual(99);
      expect(product.price).toBeLessThanOrEqual(199);
    }
  });

  it('classe les colliers avec boucles assorties dans Ensembles', () => {
    for (const id of ['ens-meandre', 'ens-serpentine', 'ens-soleil', 'ens-ovale', 'ens-marguerite']) {
      expect(products.find(product => product.id === `jj-nov26-${id}`)?.category).toBe('Ensembles');
    }
  });

  it('attribue l’étiquette Nouveau à tous les bijoux importés', () => {
    for (const product of products) expect(product.label).toBe('Nouveau');
  });
});