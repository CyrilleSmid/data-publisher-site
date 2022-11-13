using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using WPFUI.Views;
using System.Diagnostics;
using System.Data.SqlClient;

namespace WPFUI.ViewModels
{
    public class MainWindowViewModel : INotifyPropertyChanged
    {
        public MainWindowViewModel(IMainWindow view) 
        {
            Debug.WriteLine("Info: MainWindowViewModel instantiated");
            View = view;

            PrimitiveControlsView = new HomePageView();
            CurrentView = PrimitiveControlsView;
        }

        public HomePageView PrimitiveControlsView { get; set; }

        private object _currentView;
        public object CurrentView
        {
            get { return _currentView; }
            set 
            {
                _currentView = value;
                Debug.WriteLine($"Action: Current page changed to {value.ToString()}");
                RaisePropertyChanged();
            }
        }


        public IMainWindow View { get; set; }

        #region WPF Binding
        public event PropertyChangedEventHandler PropertyChanged;
        private void RaisePropertyChanged([CallerMemberName] string propertyName = null)
        {
            this.PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
        #endregion
    }
}
