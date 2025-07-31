import time
import os
import pandas as pd
import threading
import psutil
from pynvml import *
from typing import List, Dict
import matplotlib.pyplot as plt

class ResourceMonitor:
    def __init__(self, interval=5, log_path=None, verbose=False):
        """
        Initialize the ResourceMonitor with optional log persistence.
        
        Args:
            interval (int): Time interval (in seconds) between resource checks
            log_path (str): Optional path to CSV file for saving/loading logs
            verbose: Whether to print events to console
        """
        self.interval = interval
        self.log_path = log_path
        self.verbose = verbose
        self.resource_log = []
        self.event_log = []
        self.monitoring = False
        self.thread = None
        
        self._log_event("SYSTEM", "ResourceMonitor initialized")
        # Load existing log if path is provided and file exists
        if self.log_path and os.path.exists(self.log_path):
            self.load_log(silent=True)

    def _log_gpu(self):
        """
        Log GPU usage using NVIDIA Management Library (NVML).
        
        Returns:
            dict: GPU memory usage and utilization. Returns zeros if no GPU is available.
        """
        try:
            nvmlInit()
            handle = nvmlDeviceGetHandleByIndex(0)
            mem_info = nvmlDeviceGetMemoryInfo(handle)
            util_info = nvmlDeviceGetUtilizationRates(handle)
            return {
                'gpu_mem_GB': mem_info.used / (1024 ** 3),
                'gpu_util_percent': util_info.gpu
            }
        except NVMLError as e:
            self._log_event("GPU", f"NVML error: {str(e)}. Possibly no Nvidia GPUs present in the system", is_error=True)
            return {
                'gpu_mem_GB': 0.0,
                'gpu_util_percent': 0.0
            }
        finally:
            try:
                nvmlShutdown()
            except:
                pass

    def _log_resources(self):
        """
        Log system resources (CPU, RAM, GPU) at regular intervals.
        """
        while self.monitoring:
            memory = psutil.virtual_memory().used / (1024 ** 3)  # RAM in GB
            cpu_percent = psutil.cpu_percent()
            gpu_stats = self._log_gpu()

            # Append resource usage to log
            self.resource_log.append({
                'timestamp': time.time(),
                'memory_GB': memory,
                'cpu_percent': cpu_percent,
                **gpu_stats
            })
            time.sleep(self.interval)

    def _log_event(self, category, message, is_error=False):
        """Internal method to log system events"""
        event = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "message": message,
            "error": is_error
        }
        self.event_log.append(event)
        
        if self.verbose:
            status = "ERROR" if is_error else "INFO"
            print(f"[{event['timestamp']}] [{status}] {category}: {message}")


    def save_log(self, path: str = None) -> None:
        """Save metric logs to CSV"""
        try:
            save_path = path or self.log_path
            if not save_path:
                raise ValueError("No save path specified")
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            if os.path.exists(save_path):
                self._log_event("IO", f"File already exists: {save_path}. Overwriting.", is_error=False)
            
            df = self.get_logs()
            df.to_csv(save_path, index=False)
            self._log_event("IO", f"Saved {len(df)} entries to {save_path}")
            
        except Exception as e:
            self._log_event("ERROR", f"Save failed: {str(e)}", is_error=True)
            raise


    def load_log(self, path: str = None, silent: bool = False) -> None:
        """Load metric logs from CSV"""
        try:
            load_path = path or self.log_path
            if not load_path:
                raise ValueError("No load path specified")

            if os.path.exists(load_path):
                df = pd.read_csv(load_path, parse_dates=['timestamp'])
                self.resource_log = df.to_dict('records')
                msg = f"Loaded {len(df)} entries from {load_path}"
                self._log_event("IO", msg)
                if not silent:
                    print(msg)  # Always print load confirmation unless silent=True
            else:
                msg = f"File not found: {load_path}"
                self._log_event("IO", msg, is_error=True)
                if not silent:
                    print(msg)
                    
        except Exception as e:
            self._log_event("ERROR", f"Load failed: {str(e)}", is_error=True)
            raise


    def start(self, append_log=False):
        """
        Start resource monitoring.
        
        Args:
            append_log (bool): Whether to append to existing logs (False overwrites)
        """
        try:
            if self.monitoring:
                self._log_event("MONITOR", "Monitoring already in progress", is_error=True)
                raise RuntimeError("Monitoring already in progress")
            
            action = "Appending to" if append_log else "Starting new"
            self._log_event("MONITOR", f"{action} log session")

            if not append_log:
                self.resource_log.clear()
                self._log_event("DATA", "Existing logs cleared")

            self.monitoring = True
            self.thread = threading.Thread(target=self._log_resources, daemon=True)
            self.thread.start()
            self._log_event("THREAD", "Monitoring thread started")
        except Exception as e:
            self._log_event("ERROR", f"Start failed: {str(e)}", is_error=True)
            raise


    def stop(self) -> None:
        """Stop resource monitoring"""
        try:
            if self.monitoring:
                self.monitoring = False
                if self.thread is not None:
                    self.thread.join()
                    self._log_event("THREAD", "Monitoring thread stopped")
                self._log_event("MONITOR", "Stopped successfully")
            else:
                self._log_event("MONITOR", "Stop requested but not running", is_error=True)
                raise RuntimeError("Monitoring not running")
        except Exception as e:
            self._log_event("ERROR", f"Stop failed: {str(e)}", is_error=True)
            raise

    
    def get_event_log(self, filter_category: str = None) -> List[Dict]:
        """Retrieve event log with optional filtering"""
        if filter_category:
            return [e for e in self.event_log if e['category'] == filter_category]
        return self.event_log.copy()


    def get_last_event(self) -> Dict:
        """Get the most recent event"""
        return self.event_log[-1] if self.event_log else {}


    def print_event_log(self, max_events: int = 10) -> None:
        """Print recent events in readable format"""
        for event in self.event_log[-max_events:]:
            status = "ERROR" if event['error'] else "INFO"
            print(f"[{event['timestamp']}] [{status}] {event['category']}: {event['message']}")

    def get_logs(self):
        """
        Get the logged resource data as a pandas DataFrame.
        
        Returns:
            pd.DataFrame: Logged resource data.
        """
        df = pd.DataFrame(self.resource_log)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df

    def visualize_logs(self):
        """
        Visualize the logged resource data as time-series plots.
        """
        df = self.get_logs()

        if df.empty:
            print("No data to visualize.")
            return

        fig, ax = plt.subplots(3, 1, figsize=(12, 8))
        
        # Plot RAM usage
        df.plot(x='timestamp', y='memory_GB', ax=ax[0], title='RAM Usage (GB)', color='blue')
        
        # Plot CPU utilization
        df.plot(x='timestamp', y='cpu_percent', ax=ax[1], title='CPU Utilization (%)', color='orange')
        
        # Plot GPU memory usage and utilization
        df.plot(x='timestamp', y='gpu_mem_GB', ax=ax[2], title='GPU Memory Usage (GB)', color='green')
        
        plt.tight_layout()
        plt.show()

    def summarize_logs(self):
        """
        Summarize the logged resource data with key statistics.
        
        Returns:
            dict: Summary statistics of resource usage.
        """
        df = self.get_logs()
        
        if df.empty:
            print("No data to summarize.")
            return {}

        stats = {
            'Max RAM (GB)': df.memory_GB.max(),
            'Avg RAM (GB)': df.memory_GB.mean(),
            'Peak CPU (%)': df.cpu_percent.max(),
            'Max GPU Mem (GB)': df.gpu_mem_GB.max(),
            'Avg GPU Util (%)': df.gpu_util_percent.mean()
        }
        
        return stats


# Updated Example Usage:
if __name__ == "__main__":
    # Initialize with existing log path
    monitor = ResourceMonitor(interval=1, log_path="/kaggle/working/resource_log.csv", verbose=True)
    
    # Start new session (overwrite existing logs)
    monitor.start(append_log=False)
    time.sleep(30)  # Your training code
    monitor.stop()
    monitor.save_log()
    
    # Start new session while appending to previous logs
    monitor.start(append_log=True) 
    time.sleep(20)  # More training
    monitor.stop()
    monitor.save_log()
    monitor.visualize_logs()
    print(monitor.summarize_logs())
    # Load previous logs in new instance
    # new_monitor = ResourceMonitor(log_path="/kaggle/working/resource_log.csv")
    # new_monitor.visualize_logs()
