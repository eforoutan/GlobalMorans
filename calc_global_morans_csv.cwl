cwlVersion: v1.2
class: CommandLineTool

hints:
  DockerRequirement:
    dockerPull: "eforoutan/calc_global_morans:latest"
  NetworkAccess:
    networkAccess: true

inputs:
  input_shapefile:
    type:
      - File
      - Directory
    inputBinding:
      position: 1

  field_name:
    type: string
    inputBinding:
      position: 2

  weight_type:
    type:
      type: enum
      symbols:
        - "queen"
        - "rook"
    default: "queen"
    inputBinding:
      position: 3

outputs:
  output_csv:
    type: File
    outputBinding:
      glob: global_morans_results.csv  # Matches the Python script output filename