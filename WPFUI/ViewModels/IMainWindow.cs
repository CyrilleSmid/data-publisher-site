using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WPFUI.ViewModels
{
    public interface IMainWindow
    {
        public event Action OnMainWindowClosing;
    }
}
