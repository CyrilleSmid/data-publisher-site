using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace WPFUI.ViewModels
{
    public class HomePageViewModel : INotifyPropertyChanged
    {
        public HomePageViewModel(IHomePageView view)
        {
            View = view;
            Debug.WriteLine("Info: PrimitiveControlsPageViewModel instantiated");
        }

        public IHomePageView View { get; set; }

        public event Action RaiseUpdateDataBase;

        private string _name = "";
        public string Name
        {
            get { return _name; }
            set
            {
                _name = value;
                RaisePropertyChanged();
            }
        }

        private string _surname = "";
        public string Surname
        {
            get { return _surname; }
            set
            {
                _surname = value;
                RaisePropertyChanged();
            }
        }

        private string _creativeColorOutput = "";
        public string CreativeColorOutput
        {
            get { return _creativeColorOutput; }
            set
            {
                _creativeColorOutput = value;
                RaisePropertyChanged();
            }
        }

        public void OnUserIsRegistered()
        {
            RaiseUpdateDataBase?.Invoke();
        }



        #region WPF Binding
        public event PropertyChangedEventHandler PropertyChanged;
        private void RaisePropertyChanged([CallerMemberName] string propertyName = null)
        {
            this.PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
        #endregion
    }
}
