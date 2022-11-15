from .alderaan import Alderaan
import os


class MetabPrep:

    # singularity_folder = os.path.join('..','..','..','storage','singularity')
    # biotransformer_folder = os.path.join('/', 'home', 'reedsc', 'Biotransformer')
    biotransformer_folder = os.path.join('/', 'home', 'boss', 'biotransformerjar3', 'biotransformer3.0jar')

    def __init__(self, smiles):
        self.alderaan = Alderaan()
        self.smiles = smiles
        self.metab_generator = self.biotransformer(smiles)
        self.biotransformer_folder = self.biotransformer_folder

    def biotransformer(self, smiles):
        self.smile_str = str(self.smiles)
        temp_bt = 'temp'
        # biotransformer_command = f'singularity  exec biotransformer3_jar_latest.sif java -jar BioTransformer3.0_20220615.jar  -k pred -b allHuman -ismi {self.smile_str} -ocsv temp_bt_out -s 2'
        batch_file = """
            #!/bin/bash
            echo "starting biotransformer"
            #SBATCH --job-name=hello
            #SBATCH --partition=math-alderaan
            #SBATCH --time=1:00:00            # Max wall-clock time 1 hour
            #SBATCH --ntasks=2
            singularity  exec biotransformer3_jar_latest.sif java -jar BioTransformer3.0_20220615.jar -h'
        """
        # self.alderaan.send_batch(self.biotransformer_folder, batch_file)
        # chmod_command = 'chmod +x biotransformer'
        # self.alderaan.run_command(chmod_command)
        # biotransformer_command = './biotransformer'
        # biotransformer_command = f"singularity exec {self.biotransformer_folder}/biotrans3jar_latest.sif java -jar {self.biotransformer_folder}/biotransformer3.0jar/BioTransformer3.0_20220615.jar -k pred -b allHuman -ismi \"{self.smile_str}\" -ocsv bt_temp -s 2 -cm 3"

        # biotransformer_command = f'cd {self.biotransformer_folder}; java -jar BioTransformer3.0_20220615.jar -k pred' \
        #                          f'-b allHuman -ismi \"{self.smiles}\" -ocsv {temp_bt} -s 2 -a'
        biotransformer_command = f'cd {self.biotransformer_folder}; java -jar BioTransformer3.0_20220615.jar -k pred -b allHuman -ismi \"{self.smiles}\" -ocsv {temp_bt} -a'
        self.bt_output, _ = self.alderaan.run_command(biotransformer_command)
        print(self.bt_output)
        print('a')
