export interface DataTableColumn {
  index: number
  name: number
}

export interface DataTableFilter {
  columnIndex?: string
  searchText?: string
  useRegex: boolean
  useSmartSearch: boolean
}
