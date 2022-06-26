from mysite.business.alderaan import Alderaan
import os


class MetabPrep:
    smiles = ''
    # alderaan = ''
    alderaan_folder = os.path.join('/','home','reedsc')
    temp_folder = os.path.join(alderaan_folder, 'tmp')
    # singularity_folder = os.path.join('..','..','..','storage','singularity')
    biotransformer_folder = os.path.join('/','home','reedsc','Biotransformer')

    def __init__(self, smiles):
        self.alderaan = Alderaan()
        self.smiles = smiles
        self.metab_generator = self.biotransformer(smiles)
        self.biotransformer_folder = biotransformer_folder

    def biotransformer(self, smiles):
        self.smile_str = str(self.smiles)
        # self.smile_str = str(f'"{self.smile_str}"')
        # biotransformer_command = f'singularity  exec biotransformer3_jar_latest.sif java -jar BioTransformer3.0_20220615.jar  -k pred -b allHuman -ismi {self.smile_str} -ocsv temp_bt_out -s 2'
        biotransformer_command = """
            #!/bin/bash
            echo "starting biotransformer"
            #SBATCH --job-name=hello
            #SBATCH --partition=math-alderaan
            #SBATCH --time=1:00:00            # Max wall-clock time 1 hour
            #SBATCH --ntasks=2
            singularity  exec biotransformer3_jar_latest.sif java -jar BioTransformer3.0_20220615.jar -h'
        """
        biotransformer_command = f"singularity exec {self.biotransformer_folder}/biotrans3jar_latest.sif java -jar {self.biotransformer_folder}/biotransformer3.0jar/BioTransformer3.0_20220615.jar -k pred -b allHuman -ismi \"CC(C)C1=CC=C(C)C=C1O\" -ocsv bt_temp -s 2 -cm 3"
        # self.alderaan.send_batch(self.biotransformer_folder, biotransformer_command)
        # chmod_command = 'chmod +x biotransformer'
        # self.alderaan.run_command(chmod_command)
        # biotransformer_command = './biotransformer'
        bt_output, success = self.alderaan.run_command(biotransformer_command)
        print(bt_output)
