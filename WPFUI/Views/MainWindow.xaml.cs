using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using WPFUI.ViewModels;

namespace WPFUI.Views
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window, IMainWindow
    {
        public MainWindowViewModel ViewModel { get; set; }
        public MainWindow()
        {
            Debug.WriteLine("Info: MainWindow instantiated");

            InitializeComponent();

            ViewModel = new MainWindowViewModel(this);

            DataContext = ViewModel;
        }

        public event Action OnMainWindowClosing;

        private void Window_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ChangedButton == MouseButton.Left && Mouse.GetPosition(window).Y <= TopBar.Height)
            {
                this.DragMove();
            }
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        private void Minimize_Click(object sender, RoutedEventArgs e)
        {
            WindowState = WindowState.Minimized;
        }

        private void HomePage_Click(object sender, RoutedEventArgs e)
        {
            ViewModel.CurrentView = ViewModel.PrimitiveControlsView;
        }


        private void window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            OnMainWindowClosing?.Invoke();
        }

        private void SearchBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                ((TextBox)sender).Text = "I am pretty sure you can find it yourself";
                Debug.WriteLine("Action: Search fired");
            }
        }

        private void SearchBox_LostFocus(object sender, RoutedEventArgs e)
        {
            ((TextBox)sender).Text = "";
        }

        private void window_MouseMove(object sender, MouseEventArgs e)
        {
            
        }
    }
}
