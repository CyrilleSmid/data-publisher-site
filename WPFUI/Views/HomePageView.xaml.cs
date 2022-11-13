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
    /// Interaction logic for PrimitiveControlsPageView.xaml
    /// </summary>
    public partial class HomePageView : UserControl, IHomePageView
    {
        HomePageViewModel _viewModel;
        public HomePageViewModel ViewModel 
        { 
            get
            {
                return _viewModel;
            }
            set
            {
                _viewModel = value;
                DataContext = _viewModel;
            }
        }
        public HomePageView()
        {
            Debug.WriteLine("Info: PrimitiveControlsPageView instantiated");
            ViewModel = new HomePageViewModel(this);
            InitializeComponent();
        }

        private void submitRegistration_Click(object sender, RoutedEventArgs e)
        {
            // TODO: how to properly validate fields?
            SolidColorBrush highlightColor = FindResource("AccentNegative") as SolidColorBrush;
            SolidColorBrush defaultColor = FindResource("DarkAccent") as SolidColorBrush;

            if (ViewModel.Name == "")
            {
                textBoxName.Background = highlightColor;
            }
            else if(ViewModel.Surname == "")
            {
                textBoxSurname.Background = highlightColor;
            }
            else if(checkBoxAgree.IsChecked == false)
            {
                checkBoxAgree.Background = highlightColor;
            }
            else
            {
                Debug.WriteLine("Action: User registered");
                textBoxName.Background = defaultColor;
                textBoxSurname.Background = defaultColor;
                checkBoxAgree.Background = defaultColor;

                //TODO: Where to handle that
                ViewModel.OnUserIsRegistered();

            }
        }
    }
}
