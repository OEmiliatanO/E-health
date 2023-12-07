    def display_info(self):
        tex = self.get_info_by_id()
        cmd = ['python', 'check_patient.py', tex]
        try:
            self.check_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        except Exception as e:
            print("display info Error:", str(e))