# coding=utf-8
import time
import queue
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from gpiozero import Button


class MainApp(object):
    SCREEN_REFRESH_MS = 40
    MEASURE_ORDER_PADDING = (50, 0)

    class StopWatch(object):
        # GPIO input pins
        _STOPWATCH_TRIGGER_PIN = 26
        _STOPWATCH_SPLIT_TIME_TRIGGER_PIN = 19

        # Whichever pin is triggered last will stop the watch.
        # Each triggering will record data at a given moment.
        _STOPWATCH_STOP_TRIGGER_PINS = [13, 6]
        _STOPWATCH_RESET_PIN = 5

        def __init__(self):
            # Store time points from which we'll calculate delta values
            self._times = []
            self._is_running = False
            self._should_stop_clock = False

            start_button = Button(self._STOPWATCH_TRIGGER_PIN, pull_up=True, bounce_time=0.1)
            start_button.when_pressed = lambda: self._start_watch()

            split_time_button = Button(self._STOPWATCH_SPLIT_TIME_TRIGGER_PIN, pull_up=True, bounce_time=0.1)
            split_time_button.when_pressed = lambda: self._measure_split_time()

            stop_button_1 = Button(self._STOPWATCH_STOP_TRIGGER_PINS[0], pull_up=True, bounce_time=0.1)
            stop_button_1.when_pressed = lambda: self._stop_watch()

            stop_button_2 = Button(self._STOPWATCH_STOP_TRIGGER_PINS[1], pull_up=True, bounce_time=0.1)
            stop_button_2.when_pressed = lambda: self._stop_watch()

            reset_button = Button(self._STOPWATCH_RESET_PIN, pull_up=True, bounce_time=0.1)
            reset_button.when_pressed = lambda: self._reset_watch()

            self._buttons = {'start_button': start_button, 'split_time_button': split_time_button,
                             'stop_button_1': stop_button_1, 'stop_button_2': stop_button_2,
                             'reset_button': reset_button}

        @property
        def is_running(self):
            return self._is_running

        def _start_watch(self):
            self._is_running = True
            self._measure_split_time()

        def _stop_watch(self):
            self._measure_split_time()

            # This method will be triggered by two sensors.
            # The one which triggers last will stop the clock.
            if self._should_stop_clock:
                self._is_running = False
            else:
                self._should_stop_clock=True

        def _reset_watch(self):
            self._is_running = False
            self._should_stop_clock = False
            self._times = []

        def _measure_split_time(self):
            self._times.append(time.time())

        @staticmethod
        def _format_time(timedelta):
            minutes = int(int(timedelta) / 60)

            return "{0:02d}:{1:06.3f}".format(minutes, float(timedelta - (minutes * 60)))

        def get_current_time(self):
            """
            Get stopwatch time formatted as string.
            If the watch is not running and it was never started, it will return 00:00.000.
            If the watch is not running but it was started, it will return last split time.
            Otherwise it will return the time since the watch was triggered.
            """
            if self._is_running:
                return self._format_time(time.time() - self._times[0])
            elif len(self._times) > 1:
                # Do not reset stopwatch time yet. Instead show last split time.
                return self._format_time(self._times[-1] - self._times[0])
            else:
                return self._format_time(0)

    class FlowMeter(object):
        FLOW_METER_COUNT = 2

        # FIXME: Implement
        def get_current_flow(self):
            # Flow meter has pulse output –> flow is defined by number of pulses in a given time
            return 1032

        # TODO: Implement
        def get_average_flow(self):
            return 2198

        # TODO: Implement
        def reset_average_flow(self):
            pass

    class PressureTransducer(object):
        # Pressure transducer parameters:
        # - brand:              BD sensors
        # - type:               26.600G
        # - pressure range:     0–100 bar
        # - voltage output:     0–10 V DC

        PRESSURE_TRANSDUCER_COUNT = 2
        FREQ_SAMPLE = 1000

        # FIXME: Implement
        def __init__(self):
            # Init I2C bus
            # i2c = busio.I2C(board.SCL, board.SDA)

            # Create instance of AD converter module
            # adc = ADS.ADS1115(i2c)
            pass

        # FIXME: Implement
        def get_current_pressure(self):
            # Measure
            # value = adc
            # return value
            return "15/80"

    class RpmMeter(object):

        # FIXME: Implement
        def get_current_rpm(self):
            return 3152

    def __init__(self, parent):
        self._stopwatch = MainApp.StopWatch()

        self._parent = parent
        self._parent.title('Firefighter Stopwatch')
        self._parent.columnconfigure(0, weight=1)
        self._parent.rowconfigure(0, weight=1)

        # Make UI full screen
        self._parent.protocol("WM_DELETE_WINDOW", self.close)
        self._parent.focus_set()
        self._parent.attributes('-fullscreen', True)
        self._parent.bind('<KeyPress>', self.close)
        self._parent.config(cursor='none')

        # Default styles
        ttk.Style().configure('Background.TFrame', background='#EEEEEE')
        ttk.Style().configure('Customized.Stopwatch.TLabel', background='#EEEEEE', font=('Microsoft Sans Serif', 60),
                              foreground='black')
        ttk.Style().configure('Customized.Main.TLabel', background='#EEEEEE', font=('Microsoft Sans Serif', 30),
                              foreground='black')

        # Define themed main frame
        main_frame = ttk.Frame(self._parent, style='Background.TFrame')
        main_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        content_frame = ttk.Frame(main_frame, style='Background.TFrame')
        content_frame.grid(column=0, row=0)

        # Arduino Development logo
        self._arduino_logo = ImageTk.PhotoImage(file='gfx/arduino_dev_logo.png')
        arduino_logo_label = ttk.Label(content_frame, style='Customized.Main.TLabel',
                                       image=self._arduino_logo, padding=(30, 0))
        arduino_logo_label.grid(column=0, row=0, columnspan=2)

        # Stopwatch
        self._stopwatch_label = ttk.Label(content_frame, style='Customized.Stopwatch.TLabel')
        self._stopwatch_label.grid(column=2, row=0, columnspan=3)
        self._stopwatch_label['text'] = '00:00.000'

        # Automatic measurement label
        auto_measurement_label = ttk.Label(content_frame, style='Customized.Main.TLabel', padding=20)
        auto_measurement_label.grid(column=0, row=1, columnspan=5)
        auto_measurement_label['text'] = 'Automatické měření'

        # Icons
        icon_images = ['gfx/clock_icon.png', 'gfx/rpm_icon.png', 'gfx/flow_icon.png', 'gfx/pressure_icon.png']
        self._icon_refs = []  # Necessary to keep the reference in order to avoid being garbage-collected
        icon_col = 1

        for icon in icon_images:
            self._icon_refs.append(ImageTk.PhotoImage(file=icon))
            label = ttk.Label(content_frame, style='Customized.Main.TLabel', image=self._icon_refs[-1])
            label.grid(column=icon_col, row=2)
            icon_col += 1

        # Auto-measurement rows
        initial_row = 3
        self._auto_measurement_labels = {'split_times': [], 'rpm': [], 'flow': [], 'pressure': []}

        for row in range(4):
            label = ttk.Label(content_frame, style='Customized.Main.TLabel',
                              padding=self.MEASURE_ORDER_PADDING)
            label.grid(column=0, row=initial_row + row)
            label['text'] = str(row + 1)

            label = ttk.Label(content_frame, style='Customized.Main.TLabel', padding=(30, 10))
            label.grid(column=1, row=initial_row + row)
            label['text'] = '               '
            self._auto_measurement_labels['split_times'].append(label)

            label = ttk.Label(content_frame, style='Customized.Main.TLabel', padding=(30, 10))
            label.grid(column=2, row=initial_row + row)
            label['text'] = '      '
            self._auto_measurement_labels['rpm'].append(label)

            label = ttk.Label(content_frame, style='Customized.Main.TLabel', padding=(30, 10))
            label.grid(column=3, row=initial_row + row)
            label['text'] = '               '
            self._auto_measurement_labels['flow'].append(label)

            label = ttk.Label(content_frame, style='Customized.Main.TLabel', padding=(30, 10))
            label.grid(column=4, row=initial_row + row)
            label['text'] = '        '
            self._auto_measurement_labels['pressure'].append(label)

        # Manual measurement label
        label = ttk.Label(content_frame, style='Customized.Main.TLabel', padding=20)
        label.grid(column=0, row=7, columnspan=5)
        label['text'] = 'Manuální měření'

        self._manual_measurement_labels = {'split_times': [], 'rpm': [], 'flow': [], 'pressure': []}

        label = ttk.Label(content_frame, style='Customized.Main.TLabel',
                          padding=self.MEASURE_ORDER_PADDING)
        label.grid(column=0, row=8)
        label['text'] = 'M'

        label = ttk.Label(content_frame, style='Customized.Main.TLabel', padding=(30, 10))
        label.grid(column=1, row=8)
        label['text'] = '               '
        self._manual_measurement_labels['split_times'].append(label)

        label = ttk.Label(content_frame, style='Customized.Main.TLabel', padding=(30, 10))
        label.grid(column=2, row=8)
        label['text'] = '      '
        self._manual_measurement_labels['rpm'].append(label)

        label = ttk.Label(content_frame, style='Customized.Main.TLabel', padding=(30, 10))
        label.grid(column=3, row=8)
        label['text'] = '               '
        self._manual_measurement_labels['flow'].append(label)

        label = ttk.Label(content_frame, style='Customized.Main.TLabel', padding=(30, 10))
        label.grid(column=4, row=8)
        label['text'] = '        '
        self._manual_measurement_labels['pressure'].append(label)

        # Queue for UI thread to update components
        self._thread_queue = queue.Queue()
        self._parent.after(self.SCREEN_REFRESH_MS, self._update_ui)

    # noinspection PyUnusedLocal
    def close(self, *args):
        self._parent.quit()

    def _update_ui(self):
        """ Refresh UI """

        def update_ui_stopwatch_time(stopwatch_time: str):
            self._stopwatch_label['text'] = stopwatch_time

        def set_measurement_data(row=0, split_time='', rpm='', flow='', pressure='', is_manual_measure=False):
            if is_manual_measure:
                self._manual_measurement_labels['split_times'][0]['text'] = split_time
                self._manual_measurement_labels['rpm'][0]['text'] = rpm
                self._manual_measurement_labels['flow'][0]['text'] = flow
                self._manual_measurement_labels['pressure'][0]['text'] = pressure
            else:
                if row < 0 or row > 3:
                    raise ValueError("Automatic measurements have at most 4 rows!")

                self._auto_measurement_labels['split_times'][row]['text'] = split_time
                self._auto_measurement_labels['rpm'][row]['text'] = rpm
                self._auto_measurement_labels['flow'][row]['text'] = flow
                self._auto_measurement_labels['pressure'][row]['text'] = pressure

        def clear_measurement_data():
            # We put empty spaces to avoid collapsing the layout too much
            cleared_time = '               '
            cleared_rpm = '      '
            cleared_flow = '               '
            cleared_pressure = '        '

            for idx in range(4):
                set_measurement_data(row=idx, split_time=cleared_time, rpm=cleared_rpm,
                                     flow=cleared_flow, pressure=cleared_pressure,
                                     is_manual_measure=False)

            set_measurement_data(row=0, split_time=cleared_time, rpm=cleared_rpm,
                                 flow=cleared_flow, pressure=cleared_pressure,
                                 is_manual_measure=True)

        update_ui_stopwatch_time(self._stopwatch.get_current_time())

        # FIXME: Implement
        # Update data from queue
        try:
            pass

        except queue.Empty:
            pass

        self._parent.after(self.SCREEN_REFRESH_MS, self._update_ui)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    # app._set_measurement_data(time='00:00.000', rpm='3152', flow='1032/2198', pressure='15/80')
    root.mainloop()
