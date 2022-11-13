using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using WPFUI.Models;

namespace WPFUI.Handlers
{
    public class AppDataContext : DbContext
    {
        public AppDataContext()
        {

        }
        public DbSet<User> People { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder oprtionsBuilder)
        {
            if(oprtionsBuilder.IsConfigured == false)
            {
                oprtionsBuilder.UseSqlServer("Data Source=(localdb)\\MSSQLLocalDB;Initial Catalog=AppData;");
            }
        }
    }
}
