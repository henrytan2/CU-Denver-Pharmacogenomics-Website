import { PATH_NAME, paths } from '@/constants/paths'
import type { PopulationModel } from '@/models/gtexome'
import { useRefoldStore } from '@/stores/refoldStore'

const refoldStore = useRefoldStore()

export const columns = [
  {
    title: 'GeneID',
    data: 'gene_id',
    defaultContent: '',
    className: 'all'
  },
  {
    title: 'VariantID',
    data: 'variantId',
    defaultContent: '',
    className: 'all',
    visible: false
  },
  {
    title: 'Allele Frequency',
    data: 'exome.af',
    defaultContent: '',
    className: 'all'
  },
  {
    title: 'Allele Number',
    data: 'exome.an',
    defaultContent: '',
    className: 'all',
    visible: false
  },
  {
    title: 'Allele Count',
    data: 'exome.ac',
    defaultContent: '',
    className: 'all',
    visible: false
  },
  {
    title: 'Allele Count Hemi',
    data: 'exome.ac_hemi',
    defaultContent: '',
    visible: false
  },
  {
    title: 'Allele Count Homozygote',
    data: 'exome.ac_hom',
    defaultContent: '',
    className: 'all',
    visible: false
  },
  {
    title: 'Filters',
    data: 'exome.filters',
    defaultContent: '',
    className: 'all',
    visible: false
  },
  {
    title: 'African Allele Count',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: Array<PopulationModel>) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleCount = data.filter((o: any) => o.id == 'afr')[0]?.ac
      return alleleCount
    },
    className: 'all',
    visible: false
  },
  {
    title: 'African Allele Number',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleNumber = data.filter((o: any) => o.id == 'afr')[0]?.an
      return alleleNumber
    },
    className: 'all',
    visible: false
  },
  {
    title: 'African Allele Freq',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleFreq = data.filter((o: any) => o.id == 'afr')[0]?.af
      return alleleFreq
    },
    className: 'all',
    visible: false
  },
  {
    title: 'American Allele Count',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleCount = data.filter((o: any) => o.id == 'amr')[0]?.ac
      return alleleCount
    },
    className: 'all',
    visible: false
  },
  {
    title: 'American Allele Number',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleNumber = data.filter((o: any) => o.id == 'amr')[0]?.an
      return alleleNumber
    },
    className: 'all',
    visible: false
  },
  {
    title: 'American Allele Freq',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleFreq = data.filter((o: any) => o.id == 'amr')[0]?.af
      return alleleFreq
    },
    className: 'all',
    visible: false
  },
  {
    title: 'Ashkenazi Jewish Allele Count',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleCount = data.filter((o: any) => o.id == 'asj')[0]?.ac
      return alleleCount
    },
    className: 'all',
    visible: false
  },
  {
    title: 'Ashkenazi Jewish Allele Number',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleNumber = data.filter((o: any) => o.id == 'asj')[0]?.an
      return alleleNumber
    },
    className: 'all',
    visible: false
  },
  {
    title: 'Ashkenazi Jewish Allele Freq',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleFreq = data.filter((o: any) => o.id == 'asj')[0]?.af
      return alleleFreq
    },
    className: 'all',
    visible: false
  },
  {
    title: 'East Asian Allele Count',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleCount = data.filter((o: any) => o.id == 'eas')[0]?.ac
      return alleleCount
    },
    className: 'all',
    visible: false
  },
  {
    title: 'East Asian Allele Number',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleNumber = data.filter((o: any) => o.id == 'eas')[0]?.an
      return alleleNumber
    },
    className: 'all',
    visible: false
  },
  {
    title: 'East Asian Allele Freq',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleFreq = data.filter((o: any) => o.id == 'eas')[0]?.af
      return alleleFreq
    },
    className: 'all',
    visible: false
  },
  {
    title: 'Finnish Allele Count',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleCount = data.filter((o: any) => o.id == 'fin')[0]?.ac
      return alleleCount
    },
    className: 'all',
    visible: false
  },
  {
    title: 'Finnish Allele Number',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleNumber = data.filter((o: any) => o.id == 'fin')[0]?.an
      return alleleNumber
    },
    className: 'all',
    visible: false
  },
  {
    title: 'Finnish Allele Freq',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleFreq = data.filter((o: any) => o.id == 'fin')[0]?.af
      return alleleFreq
    },
    className: 'all',
    visible: false
  },
  {
    title: 'European Allele Count',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleCount = data.filter((o: any) => o.id == 'nfe')[0]?.ac
      return alleleCount
    },
    className: 'all',
    visible: false
  },
  {
    title: 'European Allele Number',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleNumber = data.filter((o: any) => o.id == 'nfe')[0]?.an
      return alleleNumber
    },
    className: 'all',
    visible: false
  },
  {
    title: 'European Allele Freq',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleFreq = data.filter((o: any) => o.id == 'nfe')[0]?.af
      return alleleFreq
    },
    className: 'all',
    visible: false
  },
  {
    title: 'Other Allele Count',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleCount = data.filter((o: any) => o.id == 'oth')[0]?.ac
      return alleleCount
    },
    className: 'all',
    visible: false
  },
  {
    title: 'Other Allele Number',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleNumber = data.filter((o: any) => o.id == 'oth')[0]?.an
      return alleleNumber
    },
    className: 'all',
    visible: false
  },
  {
    title: 'Other Allele Freq',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleFreq = data.filter((o: any) => o.id == 'oth')[0]?.af
      return alleleFreq
    },
    className: 'all',
    visible: false
  },
  {
    title: 'South Asian Allele Count',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleCount = data.filter((o: any) => o.id == 'sas')[0]?.ac
      return alleleCount
    },
    className: 'all',
    visible: false
  },
  {
    title: 'South Asian Allele Number',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleNumber = data.filter((o: any) => o.id == 'sas')[0]?.an
      return alleleNumber
    },
    className: 'all',
    visible: false
  },
  {
    title: 'South Asian Allele Freq',
    data: 'exome.populations',
    defaultContent: '',
    render: (data: any) => {
      if (!data || data.length === 0) {
        return null
      }
      const alleleFreq = data.filter((o: any) => o.id == 'sas')[0]?.af
      return alleleFreq
    },
    className: 'all',
    visible: false
  },
  {
    title: 'Flags',
    data: 'flags',
    defaultContent: '',
    className: 'all',
    visible: false
  },
  {
    title: 'Chrom',
    data: 'chrom',
    defaultContent: '',
    className: 'all',
    visible: false
  },
  {
    title: 'Pos',
    data: 'pos',
    defaultContent: '',
    className: 'all',
    visible: false
  },
  {
    title: 'Alt',
    data: 'alt',
    defaultContent: '',
    className: 'all',
    visible: false
  },
  {
    title: 'Consequence',
    data: 'consequence',
    defaultContent: '',
    className: 'all'
  },
  {
    title: 'HGVS',
    data: 'hgvs',
    defaultContent: '',
    className: 'all'
  },
  {
    title: 'HGVSc',
    data: 'hgvsc',
    defaultContent: '',
    className: 'all'
  },
  {
    title: 'HGVSp',
    data: null,
    defaultContent: '',
    className: 'all',
    render: function (data: any) {
      const CCID = data['hgvsp']
      const geneId = data['gene_id']
      let response = ''
      if (CCID != null) {
        const url = `${paths[PATH_NAME.GTEXOME]}?geneID=${geneId}&CCID=${CCID}`
        response = `<a href=${url}>${CCID}</a>`
      }
      return response
    }
  },
  {
    title: 'lof',
    data: 'lof',
    defaultContent: '',
    className: 'all'
  },
  {
    title: 'lof_filter',
    data: 'lof_filter',
    defaultContent: '',
    className: 'all',
    visible: false
  },
  {
    title: 'lof_flags',
    data: 'lof_flags',
    defaultContent: '',
    className: 'all',
    visible: false
  },
  {
    title: 'rsid',
    data: 'rsid',
    defaultContent: '',
    className: 'all',
    visible: false
  }
]
