import type { DataTableColumn } from '@/types/data-tables'
import { columns } from './data-table-columns'

const columnNamesToHide = [
  'Flags',
  'Chrom',
  'Pos',
  'Alt',
  'lof_filter',
  'lof_flags',
  'Allele Number',
  'Allele Count',
  'Allele Count Hemi',
  'Allele Count Homozygote',
  'Filters',
  'VariantID',
  'Allele Count',
  'African Allele Count',
  'African Allele Number',
  'African Allele Freq',
  'American Allele Count',
  'American Allele Number',
  'American Allele Freq',
  'Ashkenazi Jewish Allele Count',
  'Ashkenazi Jewish Allele Number',
  'Ashkenazi Jewish Allele Freq',
  'East Asian Allele Count',
  'East Asian Allele Number',
  'East Asian Allele Freq',
  'Finnish Allele Count',
  'Finnish Allele Number',
  'Finnish Allele Freq',
  'European Allele Count',
  'European Allele Number',
  'European Allele Freq',
  'Other Allele Count',
  'Other Allele Number',
  'Other Allele Freq',
  'South Asian Allele Count',
  'South Asian Allele Number',
  'South Asian Allele Freq',
  'rsid'
]

export const getHiddenColumns = (): DataTableColumn[] =>
  columns.flatMap((column, index) =>
    columnNamesToHide.includes(column.title)
      ? [
          {
            index,
            name: column.title
          } as unknown as DataTableColumn
        ]
      : []
  )
