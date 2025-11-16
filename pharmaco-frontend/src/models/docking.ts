export interface DockingModel {
  ligand: string
}

export interface DockingModelAF {
  fileName: string
  dockingLigandModels: DockingLigandModel[]
}

export interface DockingLigandModel {
  drugName: string
  smilesCode: string
}
